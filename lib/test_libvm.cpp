#include "assert.h"
#include "libvm.hpp"

int constexpr poolsize = 256 * 1024;

void test_add(int a, int b) {
  vm::VirtualMachineCpp vmcpp = vm::VirtualMachineCpp(poolsize);
  vm::int64 result;

  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(a);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(b);
  vmcpp.add_op(vm::ADD);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::EXIT);

  result = vmcpp.run(true);
  assert(result == a + b);
  std::cout << "[SCUESS] test a(" << a << ") + b(" << b << ") = " << result
            << " success!" << std::endl;
}

void test_multiply(int a, int b) {
  vm::VirtualMachineCpp vmcpp = vm::VirtualMachineCpp(poolsize);
  vm::int64 result;

  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(a);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(b);
  vmcpp.add_op(vm::MUL);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::EXIT);

  result = vmcpp.run(true);
  assert(result == a * b);
  std::cout << "[SCUESS] test a(" << a << ") * b(" << b << ") = " << result
            << " success!" << std::endl;
}

void test_string(char *s) {
  vm::VirtualMachineCpp vmcpp = vm::VirtualMachineCpp(poolsize);
  char *result;

  vmcpp.add_op(vm::IMM);
  vmcpp.add_op((vm::int64)s);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::EXIT);

  result = (char *)vmcpp.run(true);

  assert(std::string(result) == s);
  std::cout << "[SCUESS] test s(" << s << ") = " << result << " success!"
            << std::endl;
}

void test_reset_add(int a, int b, int c, int d) {
  vm::VirtualMachineCpp vmcpp = vm::VirtualMachineCpp(poolsize);
  vm::int64 result;

  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(a);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(b);
  vmcpp.add_op(vm::ADD);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::EXIT);

  result = vmcpp.run(true);
  assert(result == a + b);

  vmcpp.reset();

  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(c);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(d);
  vmcpp.add_op(vm::ADD);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::EXIT);

  result = vmcpp.run(true);
  assert(result == c + d);
  std::cout << "[SCUESS] test reset success!" << std::endl;
}

int main() {
  vm::test_cpp_connect(1);

  test_add(10, 20);
  test_add(9, -10);
  test_add(1000, -1000);

  test_multiply(1, -1);
  test_multiply(0, 100);

  test_string((char *)"123");
  test_string((char *)"456");

  test_reset_add(1, 6, 9, -100);

  return 0;
}
