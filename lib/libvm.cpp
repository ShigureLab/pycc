#include "libvm.hpp"

#include <iostream>

namespace vm {
bool test_cpp_connect(int k) {
  std::cout << "test_cpp_connect in c++ code." << std::endl;
  return true;
}
}  // namespace vm
