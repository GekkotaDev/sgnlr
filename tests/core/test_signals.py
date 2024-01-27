from src.sgnlr import signal


def test_signal_simple():
    """
    A simple sanity check if signals work with primitive data types.
    """

    count = signal(0)
    assert count() == 0

    count(count() + 2)
    assert count() == 2

    count(1)
    assert count() == 1


def test_signal_redux_like():
    """
    Tests if signals work with more complex data types.

    Within this test, we are managing the state of this graph using a methodology
    similar to the Redux pattern (but not quite). This should serve as a test to see if
    it can handle more complex data types.

    For more on the Redux pattern.
    https://redux.js.org/tutorials/essentials/part-1-overview-concepts
    """

    graph = signal(
        {
            "LAX": [],
            "CRK": [],
            "MNL": [],
        }
    )
    assert graph() == {
        "LAX": [],
        "CRK": [],
        "MNL": [],
    }

    graph(
        {
            **graph(),
            "CRK": [*graph()["CRK"], "MNL"],
            "MNL": [*graph()["MNL"], "CRK"],
        }
    )

    assert graph() == {
        "LAX": [],
        "CRK": ["MNL"],
        "MNL": ["CRK"],
    }

    graph(
        {
            **graph(),
            "MNL": [*graph()["MNL"], "LAX"],
            "LAX": [*graph()["LAX"], "MNL"],
        }
    )

    assert graph() == {
        "LAX": ["MNL"],
        "CRK": ["MNL"],
        "MNL": ["CRK", "LAX"],
    }


def test_signal_proposition():
    """
    Test if custom propositions are functioning correctly.

    This test takes advantage of object identity within Python, and how even if two
    lists seemingly have the same value they are still different objects. If the test
    were ever to fail, then either object identity has gone awry in Python or that the
    proposition implementation is not implemented correctly.
    """

    array = signal([], proposition=lambda _0, _1: True)

    assert [] is not []  # Sanity check
    assert array() is array()
    assert array() is not []

    previous = array()
    array([])

    assert array() is not previous
    assert array() is array()
    assert array() is not []
