# One executable per test file; CTest runs each and treats a non-zero exit code as failure.
add_executable(test_greeter test_greeter.cpp)
target_link_libraries(test_greeter PRIVATE myproject_core)
myproject_set_options(test_greeter)
add_test(NAME test_greeter COMMAND test_greeter)
