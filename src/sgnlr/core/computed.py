from typing import Callable, TypeVar

from .signal import signal
from . import scheduler


T = TypeVar("T")
Computation = Callable[[], T]


def computed[T](computation: Computation[T]) -> Computation[T]:
    """
    Efficiently derive a signal from the composition of other signals.

    A computed function caches the result of the computation given to it, with any calls
    to the computed function returning the cached result instead of rerunning the
    computation.

    In contrast to `lazy_computed`, a `computed` function reruns whenever any of the
    signals it is composed from changes. This allows it to update any effects that this
    is used in, though it may be excessive if only the caching behavior is needed.
    """

    def update_state():
        nonlocal state
        state(computation())

    scheduler.add(update_state)
    state = signal(computation())
    scheduler.pop()

    return state.get


def lazy_computed[T](computation: Computation[T]) -> Computation[T]:
    """
    Lazily derive a signal from the composition of other signals.

    A computed function caches the result of the computation given to it, with any calls
    to the computed function returning the cached result instead of rerunning the
    computation.

    In contrast to `computed`, a `lazy_computed` function only reruns only whenever it
    is called and if it is stale/needs to recompute. Consequentially, while this could
    reduce the overall number of computations made, this effectively makes it unable to
    rerun side effects reliably.
    """
    stale = False

    def update_state():
        nonlocal stale
        stale = True

    scheduler.add(update_state)
    state = signal(computation())
    scheduler.pop()

    def get() -> T:
        if stale:
            state(computation())

        return state()

    return get


__all__ = ("computed", "lazy_computed")
