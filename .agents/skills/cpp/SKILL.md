---
name: cpp
description: Conventions for writing, building and testing C++ with CMake (C++20, memory-safe style, commented syntax). Use whenever creating or editing .cpp/.cc/.hpp/.h files, CMakeLists.txt or CMakePresets.json, fixing compiler/linker errors or sanitizer reports, or adding C++ tests, even for small snippets.
---

# C++ (CMake)

Advisory defaults. Deviate when there is a good reason, and say why.

## Layout and build
- `include/<project>/` public headers, `src/` implementation (+ `main.cpp`), `tests/` tests.
  The template's placeholder project name is `myproject`.
- CMake >= 3.21 with **presets**, so the commands are identical on every OS:
  `cmake --preset debug`, then `cmake --build --preset debug`, then `ctest --preset debug`.
- Target-based CMake: `add_library` / `add_executable`, `target_link_libraries`,
  `target_include_directories`. No global `include_directories`, `add_definitions` or
  `CMAKE_CXX_FLAGS` edits. Warnings and sanitizers are applied per target with
  `myproject_set_options(<target>)` (defined in the root `CMakeLists.txt`).
- Standard: **C++20**, set once via `CMAKE_CXX_STANDARD` in the root `CMakeLists.txt`.
  That needs GCC 11+, Clang 14+ or MSVC 2019 16.11+. Avoid C++23-only features
  (`std::print`, `std::expected`, modules) and be careful with `<format>` (GCC 13+) unless the
  user asks. On an older toolchain, drop to C++17 and tell the user.
- New `.cpp` file: add it to the target's sources. New public header: put it in `include/<project>/`.

## Memory safety and robustness
- RAII everywhere. No raw `new`/`delete`/`malloc`/`free`. Default to `std::unique_ptr` with
  `std::make_unique`; use `std::shared_ptr` only for genuinely shared ownership. Raw pointers
  and references are non-owning only.
- Prefer `std::vector`, `std::array`, `std::string` over C arrays. For non-owning views use
  `std::span` and `std::string_view` (never return a view into a local or temporary).
- Check sizes and indices at untrusted boundaries (`at()`, explicit validation).
- `const` by default, `enum class`, `[[nodiscard]]` where ignoring a result is a bug,
  `std::optional` instead of sentinel values, `override` on virtual overrides.
- Rule of zero: let members manage themselves. If you define one special member function,
  define or delete all five.
- No C-style casts or `reinterpret_cast` (use `static_cast`). No `using namespace std;` in headers.
- Watch for dangling references, iterator invalidation, signed/unsigned comparisons, narrowing
  conversions, uninitialized variables and integer overflow.

## Comments
Add a short trailing `// ...` comment to any line whose syntax or logic is not obvious:
inheritance, templates, lambdas, operator overloads, algorithm steps, bit tricks. Lines that are
obvious (`i++`, simple assignments) need none.

```cpp
class Circle : public Shape {               // Circle inherits Shape (public inheritance = "is-a")
    double area() const override;           // override: compiler checks this matches Shape::area
};
auto it = std::find_if(v.begin(), v.end(),  // find the first element for which the lambda is true
    [](int x) { return x > 10; });          // [] captures nothing; takes an int, returns bool
```

## Verify before presenting (iterate, at most 5 attempts)
1. `cmake --preset debug` (re-run after any CMake change).
2. `cmake --build --preset debug`. Fix all errors and all warnings in code you wrote.
3. `ctest --preset debug`. The debug preset enables AddressSanitizer + UBSan on GCC/Clang
   (macOS/Linux); fix any report. On Windows/MSVC sanitizers are skipped.
4. For a lone snippet outside the project:
   `g++ -std=c++20 -Wall -Wextra -Wpedantic -fsyntax-only file.cpp`
   (`clang++` is the same; MSVC: `cl /std:c++20 /W4 /Zs file.cpp`).
Use `--preset release` only when measuring performance.

## Tests
Add or extend tests in `tests/` and register them with `add_test`. The skeleton uses plain
CTest with a tiny check helper and no dependency (`assert` is compiled out in Release, so do not
rely on it). If a framework is justified, propose Catch2 or GoogleTest via `FetchContent`
(pinned tag) and **ask first**.
