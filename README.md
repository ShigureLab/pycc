# pycc [WIP]

A simple C language compiler implemented by Python.

## Python Side

首先确保[安装 poetry](https://python-poetry.org/docs/#installation)

### Install build tools

```bash
poetry install # 首先确保 Cython 安装，如果是 Windows 需要额外自行安装 VS Build Tools
```

### Build

```bash
poetry build # 编译构建 C++ 部分
poetry install # 将 C++ 编译结果安装到 Python 代码对应位置
```

### Run

```bash
poetry run pycc
```

## C++ Side

> 未在 Windows 上进行测试

### Build

```bash
make # 编译构建 C++ 部分
```

### Run

```bash
make run # 运行 C++ 部分测试代码
```
