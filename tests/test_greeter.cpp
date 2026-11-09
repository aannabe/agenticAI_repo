// Minimal dependency-free tests. We use our own check helper instead of <cassert>, because
// assert() is compiled out in Release builds (NDEBUG) and the tests would silently pass.
#include <cstdlib>
#include <iostream>
#include <string>

#include "myproject/greeter.hpp"

namespace {

int failures = 0;  // number of failed checks; becomes the process exit code

void check_equal(const std::string& actual, const std::string& expected, int line) {
    if (actual != expected) {
        ++failures;
        std::cerr << "line " << line << ": expected \"" << expected << "\" but got \"" << actual
                  << "\"\n";
    }
}

}  // namespace

int main() {
    check_equal(myproject::make_greeting("Ada"), "Hello, Ada!", __LINE__);
    check_equal(myproject::make_greeting(""), "Hello, world!", __LINE__);  // empty-name fallback
    return failures == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
