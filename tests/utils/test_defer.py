from src.sgnlr import signal, computed
from src.sgnlr.utils import defer


def test_defer_simple():
    count = signal(0)

    squared = computed(lambda: count() * count())

    assert squared() == 0

    @defer
    def deferred():
        assert squared() == 0

        count(2)

        assert squared() == 0

    deferred()

    assert squared() == 4


def test_defer_args():
    count = signal(0)

    squared = computed(lambda: count() * count())

    assert squared() == 0

    @defer
    def deferred(value: int, equals: int):
        assert squared() == equals

        count(value)

        assert squared() == equals

    deferred(2, 0)

    assert squared() == 4
