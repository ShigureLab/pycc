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
    "CLOS", "PRTF", "MALC", "FREE", "MSET", "MCMP", "EXIT", "PLAC",
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
      this->stack + poolsize / sizeof(int64);  // BP???SP ??????????????????
  this->ax = 0;                                // ????????????????????? AX
  this->pc = text;                             // PC ???????????????????????????
  this->current_data = data;
  this->cycle = 0;  // ???????????????????????????????????????
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
  op = *(pc++);  // ??????????????????

  if (debug) {
    std::cout << logger::DEBUG_BADGE << " " << cycle << "> " << std::left
              << std::setw(4) << instruction_name[op];
    if (op <= ADJ) {  // ??????????????????????????????????????????
      std::cout << " " << *pc;
    }
    std::cout << std::endl;
  }

  // clang-format off
  switch (op) {
    case LEA: ax = (int64)(bp + *pc++); break;        // ?????????????????????
    case IMM: ax = *pc++; break;                      // ???????????????
    case JMP: pc = (int64 *)*pc; break;               // ?????????????????????
    case CALL:                                        // ??????????????????
      *--sp = (int64)(pc + 1);  // ?????????????????????
      pc = (int64 *)*pc;
      break;
    case JZ: pc = ax ? pc + 1 : (int64 *)*pc; break;  // AX ??? 0 ???????????????????????????
    case JNZ: pc = ax ? (int64 *)*pc : pc + 1; break; // AX ?????? 0 ???????????????????????????
    case ENT:                                         // ???????????????
      *--sp = (int64)bp;        // ?????????????????????
      bp = sp;                  // ????????????????????????
      sp -= *pc++;              // ?????????????????????????????????????????????
      break;
    case ADJ: sp += *pc++; break;                     // ??????????????????????????????
    case LEV:                                         // ????????????????????? ENT ?????????
      sp = bp;                  // ??????????????????????????????
      bp = (int64 *)*sp++;      // ?????????????????????????????????????????????????????????
      pc = (int64 *)*sp++;      // PC ??????????????????
      break;
    case LI: ax = *(int *)ax; break;                  // ???????????? int
    case LC: ax = *(char *)ax; break;                 // ???????????? char
    case SI: *(int *)*sp++ = ax; break;               // ???????????? int
    case SC: ax = *(char *)*sp++ = ax; break;         // ???????????? char
    case PUSH: *--sp = ax; break;                     // AX ??????

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
    VMStatusCpp status = this->step(debug);
    if (status == VMStatusCpp::EXIT) {
      return this->result_;
    }
  }
  return 0;
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

int64 VirtualMachineCpp::get_op_pointer(int offset) {
  return (int64)(this->text + this->op_counter_ + offset);
}
void VirtualMachineCpp::set_pc(int64 pc) {
  this->pc = (int64 *)pc;
}

void VirtualMachineCpp::show_ops() {
  AddressRegister op_pointer = text;
  Register op;
  int cycle = 0;
  while (op_pointer < (text + this->op_counter_)) {
    op = *op_pointer;
    std::cout << logger::INFO_BADGE << " " << cycle << "> " << std::left
              << std::setw(4) << instruction_name[op];
    if (op <= ADJ) {  // ??????????????????????????????????????????
      std::cout << " " << *++op_pointer;
    }
    std::cout << std::endl;
    op_pointer++;
    cycle++;
  }
}

void VirtualMachineCpp::setup_main(int64 main_ptr, int argc, char **argv) {
  AddressRegister tmp;
  pc = (int64 *)main_ptr;
  *--sp = EXIT;
  *--sp = PUSH;
  tmp = sp;
  *--sp = argc;
  *--sp = (int64)argv;
  *--sp = (int64)tmp;
}

}  // namespace vm
namespace common {
void _send_integer_to_pointer(vm::int64 ptr, vm::int64 value) {
  *(vm::int64 *)ptr = value;
}
}  // namespace common
