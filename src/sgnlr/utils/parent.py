from ..core.signal import signal
from ..core.effect import current


def parent_signal():
    """
    Retrieve the last updated signal.

    When used within an effect, the result in practice is this function returns one of
    the parent signals of the effect.
    """
    return signal.current


def parent_effect():
    """
    Retrieve the last ran effect.
    """
    return current
