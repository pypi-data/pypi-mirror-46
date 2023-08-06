chatora.dispatch
================

Multiple argument dispatching for Python.


## Usage
Transform a function into a dispatch generic function, such as the [functools.singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch).
Unlike the [functools.singledispatch](https://docs.python.org/3/library/functools.html#functools.singledispatch), it supports multi-dispatch.

```python
from chatora.dispatch.api import dispatch


@dispatch
def func(arg0, arg1):
    return '1st func'


assert func(0, 0) == '1st func'
assert func('0', '0') == '1st func'


@func.register
def _(arg0, arg1: int):
    return '2nd func'


assert func(0, 0) == '2nd func'
assert func('0', 0) == '2nd func'
assert func('0', '0') == '1st func'


@func.register
def _(arg0: int, arg1: int):
    return '3rd func'


assert func(0, 0) == '3rd func'
assert func('0', 0) == '2nd func'
assert func('0', '0') == '1st func'
```


It partially supports arguments with typing.Union, typing.Optioanl and typing.Any.
typing.Any is equivalent to empty annotation.

```python
from chatora.dispatch.api import dispatch
import typing


@dispatch
def func(arg0: typing.Any, arg1: typing.Any):
    return '1st func'


@func.register
def _(arg0: typing.Optional[str], arg1: typing.Union[str, list, tuple]):
    return '2nd func'


assert func(0, 0) == '1st func'
assert func('0', 0) == '1st func'
assert func('0', '0') == '2nd func'
assert func('0', []) == '2nd func'
assert func(None, ()) == '2nd func'
```


It also partially supports return type annotation.

```python
from chatora.dispatch.api import dispatch
import typing


class ResultTuple(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)


class ResultClass:
    def __init__(self, a, b):
        self.a, self.b = a, b


@dispatch
def func(arg0: typing.Optional[str], arg1: tuple):
    return '1st func'


@func.register
def _(arg0: typing.Optional[str], arg1: tuple) -> typing.Sequence[str]:
    return ['2nd', 'func']


@func.register
def _(arg0: typing.Optional[str], arg1: tuple) -> typing.Tuple[str]:
    return ('3rd', 'func')


@func.register
def _(arg0: typing.Optional[str], arg1: tuple) -> ResultTuple:
    return ResultTuple('4th', 'func')


@func.register
def _(arg0: typing.Optional[str], arg1: tuple) -> ResultClass:
    return ResultClass('4th', 'func')


assert func('0', ()) == '1st func'
assert func('0', (), _return_type=typing.Sequence[str]) == ['2nd', 'func']
assert func('0', (), _return_type=typing.Tuple[str]) == ('3rd', 'func')
assert func('0', (), _return_type=ResultTuple) == ResultTuple('4th', 'func')
assert isinstance(func('0', (), _return_type=ResultClass), ResultClass)
```

