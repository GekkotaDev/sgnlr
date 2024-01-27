from src.sgnlr import signal, computed, lazy_computed


def test_computed_simple():
    count = signal(0)

    @computed
    def squared():
        return count() * count()

    assert squared() == 0

    count(2)

    assert squared() == 4


def test_computed_nested():
    count = signal(0)

    @computed
    def squared():
        return count() * count()

    @computed
    def cubed():
        return squared() * count()

    assert cubed() == 0

    count(2)

    assert cubed() == 8


def test_computed_lambda():
    count = signal(0)

    squared = computed(lambda: count() * count())

    assert squared() == 0

    count(2)

    assert squared() == 4


def test_lazy_computed():
    count = signal(0)

    @lazy_computed
    def squared():
        return count() * count()

    assert squared() == 0

    count(2)

    assert squared() == 4


def test_lazy_computed_nested():
    count = signal(0)

    @lazy_computed
    def squared():
        return count() * count()

    @lazy_computed
    def cubed():
        return squared() * count()

    assert cubed() == 0

    count(2)

    assert cubed() == 8


def test_lazy_computed_lambda():
    count = signal(0)

    squared = lazy_computed(lambda: count() * count())

    assert squared() == 0

    count(2)

    assert squared() == 4
