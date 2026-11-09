#include <cstddef>
#include <iostream>
#include <span>
#include <string_view>

#include "myproject/greeter.hpp"

int main(int argc, char* argv[]) {
    // Wrap argv in a std::span: bounds-aware access instead of raw pointer arithmetic.
    const std::span<char*> args(argv, static_cast<std::size_t>(argc));

    // Optional first command-line argument is the name to greet (empty => default greeting).
    const std::string_view name = args.size() > 1 ? std::string_view(args[1]) : std::string_view();

    std::cout << myproject::make_greeting(name) << '\n';
    return 0;
}
