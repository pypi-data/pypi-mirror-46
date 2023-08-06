# Python Loggers , Easy to use

## Usage
1. pip install pyloggers
2. 
```python
from __future__ import (absolute_import, unicode_literals)

from pyloggers import CONSOLE



def func(a, b, c):
    CONSOLE.info("====func start . {}====".format(locals()))
    try:
        raise ValueError("value error")
    except ValueError as e:
        CONSOLE.exception(e)


def test_a():
    CONSOLE.info("==== start ===")
    func(1, 1, 1)
    CONSOLE.info("==== end ==")


def main():
    test_a()
    func(1, 1, 1)

```