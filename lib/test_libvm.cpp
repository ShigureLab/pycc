#include "assert.h"
#include "libvm.hpp"

int constexpr poolsize = 256 * 1024;

void test_add(int a, int b) {
  vm::reset_vm(poolsize);
  int i = 0;

  vm::int64 result;
  vm::text[i++] = vm::IMM;
  vm::text[i++] = a;
  vm::text[i++] = vm::PUSH;
  vm::text[i++] = vm::IMM;
  vm::text[i++] = b;
  vm::text[i++] = vm::ADD;
  vm::text[i++] = vm::PUSH;
  vm::text[i++] = vm::EXIT;

  result = vm::run_vm(true);
  assert(result == a + b);
  std::cout << "[SCUESS] test a(" << a << ") + b(" << b << ") = " << result
            << " success!" << std::endl;
}

void test_multiply(int a, int b) {
  vm::reset_vm(poolsize);
  int i = 0;

  vm::int64 result;
  vm::text[i++] = vm::IMM;
  vm::text[i++] = a;
  vm::text[i++] = vm::PUSH;
  vm::text[i++] = vm::IMM;
  vm::text[i++] = b;
  vm::text[i++] = vm::MUL;
  vm::text[i++] = vm::PUSH;
  vm::text[i++] = vm::EXIT;

  result = vm::run_vm(true);
  assert(result == a * b);
  std::cout << "[SCUESS] test a(" << a << ") * b(" << b << ") = " << result
            << " success!" << std::endl;
}

void test_string(char *s) {
  vm::reset_vm(poolsize);
  int i = 0;

  char *result;
  vm::text[i++] = vm::IMM;
  vm::text[i++] = (vm::int64)s;
  vm::text[i++] = vm::PUSH;
  vm::text[i++] = vm::EXIT;
  result = (char *)vm::run_vm(true);

  assert(std::string(result) == s);
  std::cout << "[SCUESS] test s(" << s << ") = " << result << " success!"
            << std::endl;
}

int main() {
  vm::test_cpp_connect(1);
  if (vm::init_vm(poolsize) != vm::Status::OK) {
    std::cerr << "Failed to initialize vm." << std::endl;
    return 1;
  }
  test_add(10, 20);
  test_add(9, -10);
  test_add(1000, -1000);

  test_multiply(1, -1);
  test_multiply(0, 100);

  test_string((char *)"123");
  test_string((char *)"456");

  vm::free_vm();
  return 0;
}
