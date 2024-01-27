# sgnlr

A simple, signals-based, fine grained reactive programming library. Zero external dependencies, type safe.

A basic example is provided below

```python
from sgnlr import signal, computed, effect
from snglr.utils import untrack

count = signal(0)


@computed
def squared():
    return count() * count()


@effect
def log():
    print(f"The square root of {squared()} is {untrack(count)()}")
    # The square root of 0 is 0


count(2)  # The square root of 4 is 2
```

No metaprogramming, preprocessing or hacks were used to implement this; just closures.

## Packages

| Package   | Description                       |
| --------- | --------------------------------- |
| `sgnlr` | Core reactive programming library |
|           |                                   |

## License

Apache 2.0
