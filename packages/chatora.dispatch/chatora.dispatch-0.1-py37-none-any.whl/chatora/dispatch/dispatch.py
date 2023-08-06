__all__ = (
    'dispatch',
)

from abc import get_cache_token
from itertools import chain
import functools
import inspect
import sys
import types
import typing
import weakref

# from typeguard import check_type

from chatora.dispatch.mro_resolver import compose_mro as _compose_mro


class _NotSpecified:

    __name__ = 'NOT_SPECIFIED'
    __slots__ = ()

    def __reduce__(self):
        return self.__name__

    def __str__(self):
        return f'<{self.__module__}.{self.__name__}>'

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(type(self))

    def __ne__(self, other):
        return type(self) is not type(other)

    def __bool__(self):
        return False


NOT_SPECIFIED = _NotSpecified()
_MAX_DEPTH = sys.maxsize
_NoneType = type(None)


def _find_impl(
    registry: typing.Mapping[int, typing.Mapping[typing.Tuple, typing.Callable]],
    call_types: typing.Sequence,
) -> typing.Tuple[typing.Callable, ...]:
    call_length = len(call_types)

    try:
        reg = registry[call_length]
    except KeyError:
        return ()

    lowest_depth = _MAX_DEPTH
    best_keys = []

    for reg_key in reg:
        count = 0
        depth = 0

        for pos in range(call_length):
            reg_types, ctype, r_depth = reg_key[pos], call_types[pos], _MAX_DEPTH
            if ctype is typing.Any:
                ctype = object
            elif ctype is None:
                ctype = _NoneType

            for rtype in reg_types if isinstance(reg_types, tuple) else (reg_types,):
                if isinstance(rtype, type) and isinstance(ctype, type):
                    try:
                        _d = _compose_mro(ctype, (rtype,)).index(rtype)
                        if _d < r_depth:
                            r_depth = _d
                    except ValueError:
                        continue
                elif ctype == rtype:
                    r_depth = 0
                    break
                elif pos != 0 and not isinstance(ctype, type):
                    raise TypeError(f'Invalid call type {ctype!r}')

            if r_depth < _MAX_DEPTH:
                count += 1
                depth += r_depth
            else:
                break

        if count == call_length:
            if lowest_depth > depth:
                best_keys = [reg_key]
                lowest_depth = depth
            elif lowest_depth == depth:
                best_keys.append(reg_key)

    return tuple(reg[k] for k in best_keys if k in reg)


def dispatch(
    func: typing.Callable,
    register_first_func=True,
    sub_registry_factory: typing.Callable[[], typing.Mapping] = dict,
) -> typing.Callable:
    registry = {}
    dispatch_cache = weakref.WeakValueDictionary()
    cache_token = None

    def dispatch(return_type, args: typing.Sequence, arg_types: typing.Sequence = ()):
        nonlocal cache_token

        if arg_types:
            call_types = tuple(
                object if t is typing.Any else _NoneType if return_type is None else return_type
                for t in chain((return_type,), arg_types)
            )
        else:
            call_types = tuple(chain(
                (object if return_type is typing.Any else _NoneType if return_type is None else return_type,),
                (a.__class__ for a in args),
            ))

        if cache_token is not None:
            current_token = get_cache_token()
            if cache_token != current_token:
                dispatch_cache.clear()
                cache_token = current_token
        try:
            impl = dispatch_cache[call_types]
        except KeyError:
            try:
                impl = registry[len(call_types)][call_types]
            except KeyError:
                impls = _find_impl(registry, call_types)
                if len(impls) == 1:
                    impl = impls[0]
                elif len(impls) == 0:
                    raise TypeError(
                        f'No callable found: '
                        f'arg_types={call_types[1:]!r}, return_type={call_types[0]!r}',
                    )
                elif len(impls) > 1:
                    raise TypeError(
                        f'Multiple callables found: '
                        f'arg_types={call_types[1:]!r}, return_type={call_types[0]!r}, found={impls!r}',
                    )
            dispatch_cache[call_types] = impl
        return impl

    def register(
        func: typing.Optional[typing.Callable] = None,
        arg_types: typing.Sequence = (),
        return_type: typing.Any = NOT_SPECIFIED,
    ) -> typing.Callable:
        nonlocal cache_token

        if func is None:
            return lambda func: register(func, arg_types, return_type)
        elif not hasattr(func, '__annotations__'):
            raise TypeError(
                f"Invalid first argument to `register()`: {func!r}. "
                f"Use either `@register(arg_types)` or plain `@register` "
                f"on an annotated function."
            )

        if return_type is not NOT_SPECIFIED and arg_types:
            _sig_types = chain((return_type,), arg_types)
        else:
            sig = inspect.signature(func)
            _sig_types = chain(
                (sig.return_annotation if return_type is NOT_SPECIFIED else return_type,),
                arg_types or (
                    param.annotation for param in sig.parameters.values() if param.kind in (
                        inspect.Parameter.POSITIONAL_ONLY,
                        inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    )
                ),
            )

        sig_types = []
        may_have_abstractmethods = False
        for i, t in enumerate(_sig_types):
            if t is inspect.Parameter.empty or t is typing.Any:
                t = object
            elif t is None:
                t = _NoneType
            elif isinstance(t, type):
                if hasattr(t, '__abstractmethods__'):
                    may_have_abstractmethods = True
            elif i != 0:
                # Return type can be a typing annotation. On the other hand, arg type MUST be a class,
                # typing annotation with a class __origin__, or typing.Union(with class members)

                torg = getattr(t, '__origin__', None)
                if isinstance(torg, type):
                    if getattr(t, '__args__', ()):
                        raise TypeError(f'Invalid annotation {t!r}')
                    elif hasattr(torg, '__abstractmethods__'):
                        may_have_abstractmethods = True
                    t = torg
                elif torg is typing.Union:
                    _t = []
                    for _a in t.__args__:
                        if _a is typing.Any:
                            _a = object
                        elif not isinstance(_a, type):
                            raise TypeError(f'Invalid annotation {t!r}')
                        elif hasattr(torg, '__abstractmethods__'):
                            may_have_abstractmethods = True
                        _t.append(_a)
                    t = tuple(_t)
                else:
                    raise TypeError(f'Invalid annotation {t!r}')
            sig_types.append(t)
        sig_types = tuple(sig_types)

        try:
            registry[len(sig_types)][sig_types] = func
        except KeyError:
            registry[len(sig_types)] = sub_registry_factory()
            registry[len(sig_types)][sig_types] = func

        if cache_token is None and may_have_abstractmethods:
            cache_token = get_cache_token()
        dispatch_cache.clear()
        return func

    def wrapper(*args, _return_type=typing.Any, **kwargs):
        return dispatch(_return_type, args)(*args, **kwargs)

    # funcname = getattr(func, '__name__', 'dispatch function')
    # registry[object] = func
    if register_first_func:
        register(func)
    wrapper.register = register
    wrapper.dispatch = dispatch
    wrapper.clear_dispatch_cache = dispatch_cache.clear
    wrapper._registry = types.MappingProxyType(registry)
    wrapper._dispatch_cache = dispatch_cache
    functools.update_wrapper(wrapper, func)
    return wrapper
