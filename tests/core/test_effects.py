from src.sgnlr import signal, effect, computed


def test_signal_effect():
    result = 0
    count = signal(0)

    @effect
    def _():
        nonlocal result
        result = count()

    if result:
        raise

    count(2)

    if not result:
        raise


def test_computed_effect():
    result = 0
    count = signal(0)

    @computed
    def squared():
        return count() * count()

    @effect
    def _():
        nonlocal result
        result = squared()

    if result:
        raise

    count(2)

    if not result:
        raise
