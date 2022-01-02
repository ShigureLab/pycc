#include "../include/libvm.hpp"
#include "assert.h"

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
  std::cout << logger::SCUESS_BADGE << " test a(" << a << ") + b(" << b
            << ") = " << result << " success!" << std::endl;
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
  std::cout << logger::SCUESS_BADGE << " test a(" << a << ") * b(" << b
            << ") = " << result << " success!" << std::endl;
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
  std::cout << logger::SCUESS_BADGE << " test s(" << s << ") = " << result
            << " success!" << std::endl;
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
  std::cout << logger::SCUESS_BADGE << " test reset success!" << std::endl;
}

void test_run_all_ops_add(int a, int b) {
  vm::VirtualMachineCpp vmcpp = vm::VirtualMachineCpp(poolsize);
  vm::int64 result;

  vmcpp.add_op(vm::IMM);
  vmcpp.add_op(a);
  vmcpp.add_op(vm::PUSH);
  vmcpp.add_op(vm::IMM);

  vmcpp.run_all_ops(true);
  std::cout << logger::INFO_BADGE << " Stop at here!" << std::endl;

  vmcpp.add_op(b);
  vmcpp.add_op(vm::ADD);

  vmcpp.run_all_ops(true);
  std::cout << logger::INFO_BADGE << " Stop at here!" << std::endl;

  vmcpp.add_op(vm::PUSH);

  vmcpp.run_all_ops(true);
  std::cout << logger::INFO_BADGE << " Stop at here!" << std::endl;

  vmcpp.add_op(vm::EXIT);

  result = vmcpp.run_all_ops(true);
  assert(result == a + b);
  std::cout << logger::SCUESS_BADGE << " test a(" << a << ") + b(" << b
            << ") = " << result << " success!" << std::endl;
}

int main() {
  test_add(10, 20);
  test_add(9, -10);
  test_add(1000, -1000);

  test_multiply(1, -1);
  test_multiply(0, 100);

  test_string((char *)"123");
  test_string((char *)"456");

  test_reset_add(1, 6, 9, -100);
  test_run_all_ops_add(10, 40);

  return 0;
}
