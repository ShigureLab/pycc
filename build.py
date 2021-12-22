from functools import partial
from typing import Any

from Cython.Build import cythonize
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension

ext_modules = [
    Extension(
        "pycc.vm",
        sources=["cpp/vm.pyx", "cpp/src/libvm.cpp"],
        language="c++",
    ),
]


class BuildExt(build_ext):

    compiler_flags = {
        "msvc": "/std:{std}",
        "unix": "-std={std}",
    }

    def __init__(self, *args: Any, std: str = "", **kwargs: Any):
        self.std = std
        super().__init__(*args, **kwargs)

    def build_extensions(self):
        if self.std:
            std_options = [self.compiler_flags[self.compiler.compiler_type].format(std=self.std)]
        else:
            std_options = []

        for ext in self.extensions:
            ext.extra_compile_args += std_options
            ext.extra_link_args += std_options

        super().build_extensions()


Cpp17BuildExt = partial(BuildExt, std="c++17")


def build(setup_kwargs: dict[str, Any]):
    setup_kwargs.update(
        {
            "ext_modules": cythonize(ext_modules),
            "cmdclass": {"build_ext": Cpp17BuildExt},
        }
    )
