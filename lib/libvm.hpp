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

bool test_cpp_connect(int k);

class VirtualMachineCpp {
 private:
  int op_counter_;

 public:
  AddressRegister pc;  // PC, 程序计数器
  AddressRegister bp;  // BP, 基址指针
  AddressRegister sp;  // SP, 堆栈指针
  Register ax;         // 通用寄存器
  Register cycle;
  int poolsize;

  int64 *text,    // 代码段
      *old_text,  // for dump text segment
      *stack;     // 栈区
  char *data;     // 数据段

  VirtualMachineCpp();
  VirtualMachineCpp(int poolsize);
  ~VirtualMachineCpp();
  Status _allocate_memory();
  void reset();
  void add_op(int64 op);
  int64 run(bool debug);
};

}  // namespace vm
