from src.sgnlr import signal, computed
from src.sgnlr.utils import untrack


def test_untrack_simple():
    count_a = signal(0)
    count_b = signal(0)

    sum = computed(lambda: untrack(count_a)() + count_b())

    count_a(2)
    assert sum() == 0

    count_b(2)
    assert sum() == 4
