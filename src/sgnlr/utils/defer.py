from typing import Callable, ParamSpec, TypeVar
import functools as fn

from ..core.signal import signal

P = ParamSpec("P")
T = TypeVar("T")
Batched = Callable[P, T]


def defer[**P, T](function: Batched[P, T]):
    """
    Block all side effects from running until the end of this function.

    Note that this only defers reactivity, and does not truly defer code.
    """

    @fn.wraps(function)
    def deferred(*args: P.args, **kwargs: P.kwargs):
        signal.pause = True
        value = function(*args, **kwargs)
        signal.pause = False

        for deferred in [*signal.paused]:
            deferred()

        return value

    return deferred


__all__ = ("defer",)


a = object()
