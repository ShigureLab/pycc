#include "libvm.hpp"

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

AddressRegister pc;  // PC, 程序计数器
AddressRegister bp;  // BP, 基址指针
AddressRegister sp;  // SP, 堆栈指针
Register ax;         // 通用寄存器
Register cycle;

int64 *text,    // 代码段
    *old_text,  // for dump text segment
    *stack;     // 栈区
char *data;     // 数据段

const std::string instruction_name[] = {
    "LEA",  "IMM",  "JMP",  "CALL", "JZ",   "JNZ",  "ENT",  "ADJ",
    "LEV",  "LI",   "LC",   "SI",   "SC",   "PUSH", "OR",   "XOR",
    "AND",  "EQ",   "NE",   "LT",   "GT",   "LE",   "GE",   "SHL",
    "SHR",  "ADD",  "SUB",  "MUL",  "DIV",  "MOD",  "OPEN", "READ",
    "CLOS", "PRTF", "MALC", "FREE", "MSET", "MCMP", "EXIT",
};

bool test_cpp_connect(int k) {
  std::cout << "test_cpp_connect in c++ code." << std::endl;
  return true;
}

Status init_vm(int poolsize) {
  // 分配
  if (!(text = old_text = (int64 *)std::malloc(poolsize))) {
    std::cerr << "[ERROR] Could not malloc for text area" << std::endl;
    return Status::MEMORY_ERROR;
  }
  if (!(data = (char *)std::malloc(poolsize))) {
    std::cerr << "[ERROR] Could not malloc for data area" << std::endl;
    return Status::MEMORY_ERROR;
  }
  if (!(stack = (int64 *)std::malloc(poolsize))) {
    std::cerr << "[ERROR] Could not malloc for stack area" << std::endl;
    return Status::MEMORY_ERROR;
  }

  reset_vm(poolsize);

  std::cout << "[INFO] Init vm success." << std::endl;
  return Status::OK;
}

void reset_vm(int poolsize) {
  std::memset(text, 0, poolsize);
  std::memset(data, 0, poolsize);
  std::memset(stack, 0, poolsize);

  bp = sp = stack + poolsize / sizeof(int64);  // BP、SP 初始化为栈底
  ax = 0;                                      // 清空通用寄存器 AX
  pc = text;                                   // PC 指向代码段起始地址
}

void free_vm() {
  std::free(text);
  std::free(data);
  std::free(stack);
  std::cout << "[INFO] Free vm success." << std::endl;
}

int64 run_vm(bool debug = false) {
  Register op;
  AddressRegister tmp;

  cycle = 0;
  while (true) {
    cycle++;       // 记录一共经历了多少指令周期
    op = *(pc++);  // 获取当前指令

    if (debug) {
      std::cout << cycle << "> " << std::left << std::setw(4)
                << instruction_name[op];
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
        std::cout << "exit(" << *sp << ") cycle = " << cycle << std::endl;
        return *sp;
      default: std::cerr << "[ERROR] Unknown opcode: " << op << std::endl; return -1;
    }
    // clang-format on
  }
}

}  // namespace vm
