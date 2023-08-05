from functools import reduce
from operator import mul
import typing


__all__ = [
    "markup", "compute",
]


T = typing.TypeVar("T")


def markup(var: T, num: float = 1) -> (T, dict):
    if num == 1:
        return var
    else:
        return {"$multiply": [var, num]}


def compute(oper: (T, dict)) -> T:
    if isinstance(oper, dict):
        return reduce(mul, oper["$multiply"])
    else:
        return oper
