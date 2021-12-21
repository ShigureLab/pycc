#pragma once
#include <cstring>
#include <iomanip>
#include <iostream>
#include <memory>

namespace vm {
using int64 = long long int;
using uint64 = unsigned long long int;
using Register = int64;
using AddressRegister = int64 *;

extern int64 *text,  // 代码段
    *old_text,       // for dump text segment
    *stack;          // 栈区
extern char *data;   // 数据段

enum class Status {
  OK = 0,
  MEMORY_ERROR = 1,
};

// 虚拟机指令集
// clang-format off
enum {
  LEA,  IMM,  JMP,  CALL, JZ,   JNZ,  ENT,  ADJ,
  LEV,  LI,   LC,   SI,   SC,   PUSH, OR,   XOR,
  AND,  EQ,   NE,   LT,   GT,   LE,   GE,   SHL,
  SHR,  ADD,  SUB,  MUL,  DIV,  MOD,  OPEN, READ,
  CLOS, PRTF, MALC, FREE, MSET, MCMP, EXIT,
};
// clang-format on

Status init_vm(int poolsize);
void reset_vm(int poolsize);
void free_vm();
int64 run_vm(bool debug);
bool test_cpp_connect(int k);

}  // namespace vm
