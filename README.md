# pycc <sup>[Experimental - WIP]</sup>

<p align="center">
   <a href="https://github.com/ShigureLab"><img src="https://img.shields.io/badge/ShigureLab-cyan?style=flat-square" alt="ShigureLab"></a>
   <a href="https://actions-badge.atrox.dev/ShigureLab/pycc/goto?ref=main"><img alt="Build Status" src="https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FShigureLab%2Fpycc%2Fbadge%3Fref%3Dmain&label=Tests&style=flat-square" /></a>
   <a href="https://github.com/psf/black"><img alt="black" src="https://img.shields.io/badge/code%20style-black-000000?style=flat-square"></a>
   <a href="https://gitmoji.dev"><img src="https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67?style=flat-square" alt="Gitmoji"></a>
   <a href="LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/ShigureLab/pycc?style=flat-square"></a>
</p>

A simple C language compiler implemented by Python.

## Build and Run

### Python Side

首先确保[安装 poetry](https://python-poetry.org/docs/#installation)

#### Install build tools

```bash
poetry install # 首先确保 Cython 安装，如果是 Windows 需要自行额外安装 VS Build Tools
```

#### Build

```bash
poetry build # 编译构建 C++ 部分
poetry install # 将 C++ 编译结果安装到 Python 代码对应位置
```

#### Run pycc

```bash
poetry run pycc <src>
```

#### Run tests

```bash
poetry run pytest
```

### C++ Side

> 未在 Windows 上进行测试

#### Build

```bash
make # 编译构建 C++ 部分
```

#### Run

```bash
make run # 运行 C++ 部分测试代码
```

## Directory structure

```
.
├── LICENSE
├── Makefile
├── README.md
├── build.py                        # 用于编写 Cython 构建方式
├── cpp                             # C++ 端代码（虚拟机部分）
│   ├── include                     # C++ 端头文件
│   │   └── libvm.hpp               # libvm 头文件
│   ├── libvm.pxd                   # libvm Cython 定义文件
│   ├── src                         # C++ 端源文件
│   │   └── libvm.cpp               # libvm 源文件
│   ├── test                        # C++ 端测试文件
│   │   └── test_libvm.cpp          # libvm 测试文件
│   └── vm.pyx                      # vm Cython 文件
├── poetry.lock
├── poetry.toml
├── pycc                            # Python 端代码
│   ├── __init__.py
│   ├── __main__.py                 # Python 入口文件
│   ├── vm.cpython-310-darwin.so    # vm 动态链接库，不同系统/Python 类型/Python 版本生成文件名会不同
│   └── vm.pyi                      # vm Python 定义文件（非必需，为 Editor 提供代码提示）
├── pyproject.toml
├── setup.py
├── target
│   └── test_vm                     # C++ 测试可执行文件
└── tests                           # Python 测试文件
    ├── __init__.py
    ├── test_pycc.py
    └── test_vm.py
```

其中 `cpp/include/libvm.hpp` 与 `cpp/src/libvm.cpp` 为 C++ 端代码，`cpp/libvm.pxd` 是将其对应定义引入到 Cython 文件（`cpp/vm.pyx`）中。

`cpp/vm.pyx` 是 C++ 端 libvm 的 Python 绑定，利用 Cython 连接 C++ 端代码，并将其编译成功后的动态链接库（`pycc/vm.cpython-310-darwin.so`）安装到 Python 端代码中，此时可通过 `pycc.vm` 调用。

由于 `pycc.vm` 并非 `.py` 文件，编辑器/IDE 无法通过其提供有效的代码提示，可以通过 `pycc/vm.pyi` 文件来提供 `cpp/vm.pyx` 的定义，当然，该文件并非必要。

## TODO List

-  [ ] VM
   -  [x] Python side 更多可访问的属性
   -  [x] 初始化相关测试
   -  [x] 单步调试
   -  [ ] 显示所有寄存器的方法
   -  [ ] 显示局部内存的方法
-  [ ] Lexer
-  [ ] Parser
-  [ ] docs
   -  [x] 文件结构说明
-  [x] CI

## References

-  [C4](https://github.com/rswier/c4)
-  [diy-c-compiler](https://wizardforcel.gitbooks.io/diy-c-compiler/content/1.html)
