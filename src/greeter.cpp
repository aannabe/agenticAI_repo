#include "myproject/greeter.hpp"

namespace myproject {

std::string make_greeting(std::string_view name) {
    if (name.empty()) {      // avoid producing "Hello, !"
        name = "world";      // the view now points at a string literal (static storage, no copy)
    }
    // string_view has no operator+, so copy the view into a std::string before concatenating.
    return "Hello, " + std::string(name) + "!";
}

}  // namespace myproject
