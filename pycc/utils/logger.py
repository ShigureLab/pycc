from ansimarkup import parse
from typing import Any

INFO_BADGE = parse("<light-blue> INFO </light-blue>")
WARNING_BADGE = parse("<yellow> WARN </yellow>")
ERROR_BADGE = parse("<bold><red> ERROR </red></bold>")
DEBUG_BADGE = parse("<green> DEBUG </green>")
SCUESS_BADGE = parse("<black><GREEN> SCUESS </GREEN></black>")
FAIL_BADGE = parse("<black><RED> FAIL </RED></black>")


def info(string: Any, *print_args: Any, **print_kwargs: Any):
    print(INFO_BADGE, string, *print_args, **print_kwargs)


def warn(string: Any, *print_args: Any, **print_kwargs: Any):
    print(WARNING_BADGE, string, string, *print_args, **print_kwargs)


def error(string: Any, *print_args: Any, **print_kwargs: Any):
    print(ERROR_BADGE, string, *print_args, **print_kwargs)


def debug(string: Any, *print_args: Any, **print_kwargs: Any):
    print(DEBUG_BADGE, string, *print_args, **print_kwargs)


def scuess(string: Any, *print_args: Any, **print_kwargs: Any):
    print(SCUESS_BADGE, string, *print_args, **print_kwargs)


def fail(string: Any, *print_args: Any, **print_kwargs: Any):
    print(FAIL_BADGE, string, *print_args, **print_kwargs)
