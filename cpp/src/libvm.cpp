#include "../include/libvm.hpp"

#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include <iostream>

namespace vm {

// +------------------+
// |    stack   |     |      high address
// |    ...     v     |
// |                  |  <-- BP
// |                  |  <-- SP
// |                  |
// |                  |
// |    ...     ^     |
// |    heap    |     |
// +------------------+
// |                  |
// | bss  segment     |
// |                  |
// +------------------+
// |                  |
// | data segment     |
// |                  |
// +------------------+
// |                  |
// | text segment     |      low address
// |                  |  <-- PC
// +------------------+

const std::string instruction_name[] = {
    "LEA",  "IMM",  "JMP",  "CALL", "JZ",   "JNZ",  "ENT",  "ADJ",
    "LEV",  "LI",   "LC",   "SI",   "SC",   "PUSH", "OR",   "XOR",
    "AND",  "EQ",   "NE",   "LT",   "GT",   "LE",   "GE",   "SHL",
    "SHR",  "ADD",  "SUB",  "MUL",  "DIV",  "MOD",  "OPEN", "READ",
    "CLOS", "PRTF", "MALC", "FREE", "MSET", "MCMP", "EXIT",
};

VirtualMachineCpp::VirtualMachineCpp() {
}

VirtualMachineCpp::VirtualMachineCpp(int poolsize) {
  this->poolsize = poolsize;
  if (this->_allocate_memory() == Status::OK) {
    std::cout << logger::INFO_BADGE << " Init vm success." << std::endl;
  }
  this->reset();
}

VirtualMachineCpp::~VirtualMachineCpp() {
  std::free(this->text);
  std::free(this->data);
  std::free(this->stack);
  std::cout << logger::INFO_BADGE << " Free vm success." << std::endl;
}

Status VirtualMachineCpp::_allocate_memory() {
  if (!(this->text = old_text = (int64 *)std::malloc(poolsize))) {
    std::cerr << logger::ERROR_BADGE << " Could not malloc for text area"
              << std::endl;
    return Status::MEMORY_ERROR;
  }
  if (!(this->data = (char *)std::malloc(poolsize))) {
    std::cerr << logger::ERROR_BADGE << " Could not malloc for data area"
              << std::endl;
    return Status::MEMORY_ERROR;
  }
  if (!(this->stack = (int64 *)std::malloc(poolsize))) {
    std::cerr << logger::ERROR_BADGE << " Could not malloc for stack area"
              << std::endl;
    return Status::MEMORY_ERROR;
  }
  return Status::OK;
}

void VirtualMachineCpp::reset() {
  std::memset(this->text, 0, this->poolsize);
  std::memset(this->data, 0, this->poolsize);
  std::memset(this->stack, 0, this->poolsize);

  this->op_counter_ = 0;
  this->status = VMStatusCpp::INIT;
  this->bp = this->sp =
      this->stack + poolsize / sizeof(int64);  // BP、SP 初始化为栈底
  this->ax = 0;                                // 清空通用寄存器 AX
  this->pc = text;                             // PC 指向代码段起始地址
  this->current_data = data;
  this->cycle = 0;  // 记录一共经历了多少指令周期
}

void VirtualMachineCpp::add_op(int64 op) {
  this->text[this->op_counter_++] = op;
  if (this->op_counter_ > this->poolsize) {
    std::cerr << "[ERROR] op counter overflow" << std::endl;
  }
}

int64 VirtualMachineCpp::put_int_onto_data(int value) {
  int64 current_ptr = (int64)this->current_data;
  *(int *)this->current_data = value;
  this->current_data += sizeof(int);
  return current_ptr;
}

VMStatusCpp VirtualMachineCpp::step(bool debug = false) {
  Register op;
  AddressRegister tmp;

  if (this->status == VMStatusCpp::INIT) {
    this->status = VMStatusCpp::RUNNING;
  }
  this->cycle++;
  op = *(pc++);  // 获取当前指令

  if (debug) {
    std::cout << logger::DEBUG_BADGE << " " << cycle << "> " << std::left
              << std::setw(4) << instruction_name[op];
    if (op <= ADJ) {  // 含操作数指令，额外打印操作数
      std::cout << " " << *pc;
    }
    std::cout << std::endl;
  }

  // clang-format off
  switch (op) {
    case LEA: ax = (int64)(bp + *pc++); break;        // 加载地址或参数
    case IMM: ax = *pc++; break;                      // 加载立即数
    case JMP: pc = (int64 *)*pc; break;               // 跳转到指定地址
    case CALL:                                        // 跳转到子程序
      *--sp = (int64)(pc + 1);  // 将返回地址压栈
      pc = (int64 *)*pc;
      break;
    case JZ: pc = ax ? pc + 1 : (int64 *)*pc; break;  // AX 为 0 时跳转至操作数位置
    case JNZ: pc = ax ? (int64 *)*pc : pc + 1; break; // AX 为非 0 时跳转至操作数位置
    case ENT:                                         // 进入子程序
      *--sp = (int64)bp;        // 将基址指针压栈
      bp = sp;                  // 基址指针指向栈顶
      sp -= *pc++;              // 栈顶指针向下移动（有几个参数）
      break;
    case ADJ: sp += *pc++; break;                     // 根据立即数调节栈指针
    case LEV:                                         // 离开子程序（与 ENT 相对）
      sp = bp;                  // 栈顶指针退到基址指针
      bp = (int64 *)*sp++;      // 基址指针指向原基址地址（恢复基址指针）
      pc = (int64 *)*sp++;      // PC 指向返回地址
      break;
    case LI: ax = *(int *)ax; break;                  // 加载一个 int
    case LC: ax = *(char *)ax; break;                 // 加载一个 char
    case SI: *(int *)*sp++ = ax; break;               // 存储一个 int
    case SC: ax = *(char *)*sp++ = ax; break;         // 存储一个 char
    case PUSH: *--sp = ax; break;                     // AX 压栈

    case OR:  ax = *sp++ |  ax; break;
    case XOR: ax = *sp++ ^  ax; break;
    case AND: ax = *sp++ &  ax; break;
    case EQ:  ax = *sp++ == ax; break;
    case NE:  ax = *sp++ != ax; break;
    case LT:  ax = *sp++ <  ax; break;
    case GT:  ax = *sp++ >  ax; break;
    case LE:  ax = *sp++ <= ax; break;
    case GE:  ax = *sp++ >= ax; break;
    case SHL: ax = *sp++ << ax; break;
    case SHR: ax = *sp++ >> ax; break;
    case ADD: ax = *sp++ +  ax; break;
    case SUB: ax = *sp++ -  ax; break;
    case MUL: ax = *sp++ *  ax; break;
    case DIV: ax = *sp++ /  ax; break;
    case MOD: ax = *sp++ %  ax; break;

    case OPEN: ax = open((char *)sp[1], sp[0]); break;
    case READ: ax = read(sp[2], (char *)sp[1], sp[0]); break;
    case CLOS: ax = close(sp[0]); break;
    case PRTF:
      tmp = sp + pc[1];
      ax = printf((char *)tmp[-1], tmp[-2], tmp[-3], tmp[-4], tmp[-5], tmp[-6]);
      break;
    case MALC: ax = (int64)malloc(sp[0]); break;
    case FREE: free((void *)sp[0]); break;
    case MSET: ax = (int64)memset((char *)sp[2], sp[1], sp[0]); break;
    case MCMP: ax = (int64)memcmp((char *)sp[2], (char *)sp[1], sp[0]); break;
    case EXIT:
      std::cout << "exit(" << *sp << ") cycle = " << this->cycle << std::endl;
      this->status = VMStatusCpp::EXIT;
      this->result_ = *sp;
      break;
    default:
      std::cerr << "[ERROR] Unknown opcode: " << op << std::endl;
      this->status = VMStatusCpp::ERROR;
  }

  return this->status;
  // clang-format on
}

int64 VirtualMachineCpp::run(bool debug = false) {
  while (true) {
    int oplen = *(this->pc) <= ADJ ? 2 : 1;
    if (this->pc_offset() + oplen <= this->op_counter_) {
      VMStatusCpp status = this->step(debug);
      if (status == VMStatusCpp::EXIT) {
        return this->result_;
      }
    } else {
      std::cout << logger::WARNING_BADGE << " pc out of op_counter"
                << std::endl;
    }
  }
}

int64 VirtualMachineCpp::run_all_ops(bool debug = false) {
  while (true) {
    int oplen = *(this->pc) <= ADJ ? 2 : 1;
    if (this->pc_offset() + oplen <= this->op_counter_) {
      VMStatusCpp status = this->step(debug);
      if (status == VMStatusCpp::EXIT) {
        break;
      }
    } else {
      break;
    }
  }
  return this->result_;
}

int VirtualMachineCpp::pc_offset() {
  return pc - text;
}
}  // namespace vm
