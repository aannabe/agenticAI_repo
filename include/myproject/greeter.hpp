#pragma once  // include this header at most once per translation unit

#include <string>
#include <string_view>

namespace myproject {

// Builds a greeting such as "Hello, Ada!". An empty name falls back to "world".
// Takes std::string_view so callers can pass string literals or std::string without copying.
std::string make_greeting(std::string_view name);

}  // namespace myproject
