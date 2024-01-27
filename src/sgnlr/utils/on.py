from typing import Any, Callable

from ..core.effect import effect
from .untrack import untrack


def on(*signals: Callable[[], Any]):
    """
    Declare an effect with explicit dependencies.

    The declared side effect will only rerun whenever any signal within the signals list
    has changed, and not when any signal within the effect itself has changed. This can
    be used to specifiy only which signals should rerun the side effect.

    If no signals has been explicitly declared, the effect will only run once.
    """

    def function[T](function: Callable[[], T]) -> Callable[[], T]:
        @effect
        def _():
            for signal in signals:
                signal()

            @untrack
            def _():
                function()

        return function

    return function
