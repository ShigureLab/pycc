#pragma once
#include <cstring>
#include <iomanip>
#include <iostream>
#include <memory>

namespace logger {
const std::string INFO_BADGE = "\x1b[94m INFO \x1b[0m";
const std::string WARNING_BADGE = "\x1b[33m WARN \x1b[0m";
const std::string ERROR_BADGE = "\x1b[1m\x1b[31m ERROR \x1b[0m\x1b[1m\x1b[0m";
const std::string DEBUG_BADGE = "\x1b[32m DEBUG \x1b[0m";
const std::string SCUESS_BADGE =
    "\x1b[30m\x1b[42m SCUESS \x1b[0m\x1b[30m\x1b[0m";
const std::string FAIL_BADGE = "\x1b[30m\x1b[41m FAIL \x1b[0m\x1b[30m\x1b[0m";

}  // namespace logger

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
  CLOS, PRTF, MALC, FREE, MSET, MCMP, EXIT, PLAC,
};
// clang-format on

enum class VMStatusCpp {
  INIT = 0,
  RUNNING = 1,
  EXIT = 2,
  ERROR = 3,
};

class VirtualMachineCpp {
 private:
  int op_counter_;
  int64 result_;

 public:
  AddressRegister pc;  // PC, 程序计数器
  AddressRegister bp;  // BP, 基址指针
  AddressRegister sp;  // SP, 堆栈指针
  Register ax;         // 通用寄存器
  Register cycle;
  int poolsize;
  VMStatusCpp status;

  int64 *text,        // 代码段
      *old_text,      // for dump text segment
      *stack;         // 栈区
  char *data,         // 数据段
      *current_data;  // 当前数据指针

  VirtualMachineCpp();
  VirtualMachineCpp(int poolsize);
  ~VirtualMachineCpp();
  Status _allocate_memory();
  void reset();
  void add_op(int64 op);
  int64 put_int_onto_data(int value);
  VMStatusCpp step(bool debug);
  int64 run(bool debug);
  int64 run_all_ops(bool debug);
  int pc_offset();
  int64 get_op_pointer(int offset);
  void set_pc(int64 pc);
  void show_ops();
  void setup_main(int64 main_ptr, int argc = 0, char **argv = nullptr);
};

}  // namespace vm

namespace common {
using int64 = long long int;
void _send_integer_to_pointer(vm::int64 ptr, vm::int64 value);
}  // namespace common
