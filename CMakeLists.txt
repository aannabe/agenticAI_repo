cmake_minimum_required(VERSION 3.21)              # 3.21 is needed for CMakePresets.json (version 3)
project(myproject VERSION 0.1.0 LANGUAGES CXX)    # rename "myproject" when you start a new project

# ---- C++ standard: change it here, and only here ---------------------------------------------
set(CMAKE_CXX_STANDARD 20)             # C++20: widely supported (GCC 11+, Clang 14+, MSVC 2019 16.11+)
set(CMAKE_CXX_STANDARD_REQUIRED ON)    # fail instead of silently falling back to an older standard
set(CMAKE_CXX_EXTENSIONS OFF)          # use -std=c++20 rather than -std=gnu++20 (more portable)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # write build/<preset>/compile_commands.json for editors/tools

option(MYPROJECT_SANITIZE "Enable AddressSanitizer + UBSan (GCC/Clang on macOS/Linux)" OFF)
option(MYPROJECT_BUILD_TESTS "Build the tests in tests/" ON)

# ---- Per-target warnings and sanitizers -------------------------------------------------------
# Call myproject_set_options(<target>) for every target you create.
function(myproject_set_options target)
  if(MSVC)
    target_compile_options(${target} PRIVATE /W4 /permissive-)
  else()
    target_compile_options(${target} PRIVATE -Wall -Wextra -Wpedantic -Wshadow -Wconversion)
  endif()

  # Sanitizers catch memory errors and undefined behavior at run time (not available on Windows).
  if(MYPROJECT_SANITIZE AND NOT MSVC AND NOT WIN32)
    target_compile_options(${target} PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
    target_link_options(${target} PRIVATE -fsanitize=address,undefined)
  endif()
endfunction()

# ---- Targets ----------------------------------------------------------------------------------
# Library with the real logic; both the executable and the tests link against it.
add_library(myproject_core src/greeter.cpp)
target_include_directories(myproject_core PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>)
myproject_set_options(myproject_core)

add_executable(myproject src/main.cpp)
target_link_libraries(myproject PRIVATE myproject_core)
myproject_set_options(myproject)

# ---- Tests (CTest) ----------------------------------------------------------------------------
if(MYPROJECT_BUILD_TESTS)
  enable_testing()          # must be called in the top-level CMakeLists for `ctest` to find tests
  add_subdirectory(tests)
endif()
