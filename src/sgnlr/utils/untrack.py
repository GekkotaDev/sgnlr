from typing import Callable, TypeVar

from ..core import scheduler

T = TypeVar("T")
Code = Callable[[], T]


def noop():
    pass


def untrack[T](code: Code[T]) -> Callable[[], T]:
    """
    Exclude a function or a signal from the reactivity system, making it non-reactive.

    Under the hood, it presents itself to the scheduler as the same no op (no operation)
    function; the effect in practice makes the code inside `untrack` non-reactive.
    """
    scheduler.add(noop)
    value = code()
    scheduler.pop()

    return lambda: value


ref = untrack


__all__ = ("untrack", "ref")
