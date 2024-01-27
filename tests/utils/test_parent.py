from src.sgnlr import signal, effect
from src.sgnlr.utils import parent_signal


def test_parent_signal():
    count = signal(0)
    temporary = signal(0)
    result = parent_signal()

    assert result == temporary

    @effect
    def _():
        nonlocal result
        result = parent_signal()
        count()

    count(2)
    assert result == count
