# TODO: Migrate to separate package.
from typing import Callable, TypeVar

from ..core.signal import signal


Action = TypeVar("Action")
Type = TypeVar("Type")

Reducer = Callable[[Type, Action], Type]

State = signal[Type]
Dispatcher = Callable[[Action], None]
Methods = Callable[[], tuple[State[Type], Dispatcher[Action]]]

ReducerDecorator = Callable[[Reducer[Type, Action]], Methods[Type, Action]]


def reducer[A, T](initial_value: T | signal[T]) -> ReducerDecorator[T, A]:
    """
    Create a managed, read-only signal.

    Reducers may be used to simplify the management of complex state within signals. It
    achieves this through a declarative API and immutability.

    Instead of directly writing to the state of the signal, messages are dispatched to
    the reducer that tells it the result that is expected, leaving the details of how it
    should be updated to that result to the reducer itself. This frees the caller from
    the responsibility of managing state.

    Additionally, reducers enforce function purity and idempotency at runtime by testing
    for object identity & running the reducer twice in debug mode, failing if the result
    of both runs are not equal. In turn, state changes are then made predictable.
    """

    if not isinstance(initial_value, signal):
        initial_value = signal(initial_value)

    def function(reducer: Reducer[T, A]) -> Methods[T, A]:
        state: signal[T] = initial_value

        def dispatcher(action: A):
            result = reducer(state(), action)

            if __debug__ and reducer(state(), action) is result:
                raise

            if result is not state():
                state(result)

        return lambda: (state, dispatcher)

    return function


__all__ = ("signal",)
