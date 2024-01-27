from typing import Any, Callable


Dependency = Callable[[], Any]


dependency_stack: list[Dependency] = []


def add(dependency: Dependency):
    if dependency not in dependency_stack:
        dependency_stack.append(dependency)


def pop():
    return dependency_stack.pop()


def at(index: int) -> Callable[[], None] | None:
    if len(dependency_stack) < 1:
        return None

    return dependency_stack[index]


__all__ = ("add", "pop", "at")
