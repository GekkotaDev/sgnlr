from typing import Any, Callable, ParamSpec, TypeVar

from . import scheduler


P = ParamSpec("P")
T = TypeVar("T")
Batched = Callable[P, T]
Proposition = Callable[[T, T], bool]
Observer = Callable[[], Any]
Deferred = Callable[[], None]


class signal[T]:
    """
    An object whose state may change over the course of time.

    Signals are one of the core primitives within `sgnlr`, alongside `effect` and
    `computed`. They enable an easy use of reactive programming, a declarative method
    of modelling the state and changes of your application.
    """

    current: "signal[Any]"
    paused: set[Deferred] = set()
    pause = False
    proposition: Proposition[T] = lambda old, new: old != new

    value: T
    observers: set[Observer]

    def __init__(self, value: T, *, proposition: Proposition[T] | None = None):
        """
        Set the initial value of the signal.

        A proposition function may optionally be provided. The function takes in the old
        value and the new value, and if it returns true will update the signal.
        """

        self.value = value
        self.observers = set()

        if proposition:
            self.proposition = proposition

        signal.current = self

    def __call__(self, new: None | T = None) -> T:
        """
        Operate on the value of the signal.

        This combines the functionality of the `.get` and `.set` methods, and provides
        a concise, short syntax.
        """
        value = self.get()

        if new is not None:
            self.set(new)
            return self.value

        return value

    def get(self) -> T:
        """
        Explicitly retrieve the current value of the signal.

        This may be used when explicitness is more desirable, whether it is out of
        personal preference, narrowing down the type of a signal, limiting access to the
        signal to be read only, or for another reason.
        """
        observer = scheduler.at(-1)

        if observer:
            self.observers.add(observer)

        return self.value

    def set(self, new: T):
        """
        Explicitly set the current value of the signal.

        This may be used either as a personal preference to explicitly setting the value
        of the signal, to limit access to the signal to be write only, or while not
        recommended to update the value of the signal within an effect.
        """
        self.value = new

        if signal.pause:
            signal.paused.add(self.update)
            return

        self.update()

    def update(self):
        """
        Manually rerun all effects dependent on this signal.
        """
        signal.current = self

        for observer in self.observers:
            observer()

    def free(self, observer: Observer | None = None):
        """
        Free the signal responsibility of any effects dependent on it.

        Note that this does not automatically free up all effects dependent on it from
        being rerun, it merely frees them from being rerun by this signal.

        It is normally not advised to use this method, and is only provided as a
        convenience hook for library and framework authors to use.
        """
        if observer:
            self.observers.remove(observer)
            return

        self.observers.clear()


__all__ = ("signal",)
