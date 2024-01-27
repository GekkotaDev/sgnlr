from src.sgnlr import signal
from src.sgnlr.utils import on


def test_on_simple():
    sum = 0
    count_a = signal(0)
    count_b = signal(0)

    @on(count_b)
    def _():
        nonlocal sum
        sum = count_a() + count_b()

    if sum:
        raise

    count_a(2)
    if sum:
        raise

    count_b(2)
    if not sum:
        raise
