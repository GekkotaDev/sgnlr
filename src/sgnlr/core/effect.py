from typing import Callable

from . import scheduler


Callback = Callable[[], None]


current: Callback = lambda: None


def effect(effect: Callback):
    """
    Create a side effect that runs whenever a signal inside it changes.

    Side effects allow for a concise description of changes that should occur whenever
    a signal/multiple signals update. Consequentially because of this behavior, it is
    recommended that signals inside an effect should be read only, to use a `computed`
    function instead, or to use the `on` utility instead.

    If it is necessary that the same signal must be read from and written to within an
    effect, then extra care must be taken to avoid unnecessary reruns of the effect.
    Utilities such as `untrack` and `defer` may be used to assist with this.

    For users coming from React, not only is a dependency array not needed but it is not
    available to begin with. Dependencies are automatically tracked.
    """

    def update_state():
        global current

        current = update_state
        effect()

    scheduler.add(update_state)
    update_state()
    scheduler.pop()

    return effect


__all__ = ("effect", "current")
