__all__ = (
    'Reify',
    'reify',
    'reduce_decorators',
    'isplit_n',
    'merge_ordered',
    'deco_singleton',
    'mangle_cls_attr_map',
)

import functools
from inspect import isfunction
from itertools import (
    chain,
    filterfalse,
    islice,
)
import threading
import typing


T = typing.TypeVar('T')


class Reify:

    def __init__(self, fget: typing.Callable) -> None:
        functools.update_wrapper(wrapper=self, wrapped=fget, assigned=functools.WRAPPER_ASSIGNMENTS, updated=())
        self._fget = fget
        return

    def __get__(self, instance: typing.Optional[T], owner: type):
        if instance is None:
            return self
        else:
            value = self._fget(instance)
            setattr(instance, self._fget.__name__, value)
            return value

    def __repr__(self):
        return repr(self._fget)


reify: typing.Type[Reify] = Reify


class Reifiable:

    def __init__(self, fget: typing.Callable[[T], typing.Any]) -> None:
        functools.update_wrapper(wrapper=self, wrapped=fget, assigned=functools.WRAPPER_ASSIGNMENTS, updated=())
        self._fget = fget
        return

    def __get__(self, instance: typing.Optional[T], owner: type):
        if instance is None:
            return self
        else:
            value = self._fget(instance)
            return value

    def __repr__(self):
        return repr(self._fget)


reifiable: typing.Type[Reifiable] = Reifiable


def reduce_decorators(decorators: typing.Iterable[typing.Callable]) -> typing.Callable:
    def _reduce_decorators(wrapped: typing.Callable):
        return functools.reduce(
            lambda _wrapped, _deco: _deco(_wrapped),
            decorators,
            wrapped,
        )
    return _reduce_decorators


def isplit_n(iterable: typing.Iterable[typing.Any], n: int) -> typing.Iterable[typing.Any]:
    iter_ = iter(iterable)
    chunk = tuple(islice(iter_, n))
    while chunk:
        yield chunk
        chunk = tuple(islice(iter_, n))


def merge_ordered(ordereds: typing.Iterable[typing.Any]) -> typing.Iterable[typing.Any]:
    """Merge multiple ordered so that within-ordered order is preserved
    """
    seen_set = set()
    add_seen = seen_set.add
    return reversed(tuple(map(
        lambda obj: add_seen(obj) or obj,
        filterfalse(
            seen_set.__contains__,
            chain.from_iterable(map(reversed, reversed(ordereds))),
        ),
    )))


def deco_singleton(
    klass: typing.Optional[type] = None,
    lock_factory: typing.Callable = threading.Lock,
) -> typing.Union[type, typing.Callable]:
    if klass is None:
        return lambda _klass: deco_singleton(
            klass=_klass,
            lock_factory=lock_factory,
        )

    if hasattr(klass, '_x_singleton_i_lock') is True:
        raise TypeError(
            f'Can not decorate {klass!r} with class-base singleton'
            f' which is already equipped with instance-base singleton.',
        )
    elif hasattr(klass, '_x_singleton_c_lock') is False:
        if '__new__' in klass.__dict__:
            raise TypeError(
                f'Can not decorate {klass!r} with singleton, since `super()` may be used in the `__new__`.',
            )

        def __new__(cls, *args, **kwargs):
            if type(cls.__dict__.get('_x_singleton_c_info')) is not cls:
                with cls._x_singleton_c_lock:
                    if type(cls.__dict__.get('_x_singleton_c_info')) is not cls:
                        if '_x_singleton_c_info' not in cls.__dict__:
                            cls._x_singleton_c_info = None
                        if '_x_singleton_c_lock' not in cls.__dict__:
                            cls._x_singleton_c_lock = lock_factory()
                        cls._x_singleton_c_info = super(klass, cls).__new__(cls, *args, **kwargs)
            return cls._x_singleton_c_info

        klass.__new__ = __new__
    if '_x_singleton_c_info' not in klass.__dict__:
        klass._x_singleton_c_info = None
    if '_x_singleton_c_lock' not in klass.__dict__:
        klass._x_singleton_c_lock = lock_factory()
    return klass


def deco_instance_singleton(
    klass: typing.Optional[type] = None,
    key_name: str = 'x_instance_key',
    lock_factory: typing.Callable = threading.Lock,
) -> typing.Union[type, typing.Callable]:
    if klass is None:
        return lambda _klass: deco_instance_singleton(
            klass=_klass,
            key_name=key_name,
            lock_factory=lock_factory,
        )
    if hasattr(klass, '_x_singleton_c_lock') is True:
        raise TypeError(
            f'Can not decorate {klass!r} with instance-base singleton'
            f' which is already equipped with class-base singleton',
        )
    elif hasattr(klass, '_x_singleton_i_lock') is False:
        if '__new__' in klass.__dict__:
            raise TypeError(
                f'Can not decorate {klass!r} with singleton, since `super()` may be used in the `__new__`.'
            )

        def __new__(cls, *args, **kwargs):
            key = kwargs.pop(key_name, None)
            if key is None:
                return super(klass, cls).__new__(cls, *args, **kwargs)
            if type(cls.__dict__.get('_x_singleton_i_info', {}).get(key)) is not cls:
                with cls._x_singleton_i_lock:
                    if type(cls.__dict__.get('_x_singleton_i_info', {}).get(key)) is not cls:
                        if '_x_singleton_i_info' not in cls.__dict__:
                            cls._x_singleton_i_info = {}
                        if '_x_singleton_i_lock' not in cls.__dict__:
                            cls._x_singleton_i_lock = lock_factory()
                        cls._x_singleton_i_info[key] = super(klass, cls).__new__(cls, *args, **kwargs)
            return cls._x_singleton_i_info[key]

        klass.__new__ = __new__
    if '_x_singleton_i_info' not in klass.__dict__:
        klass._x_singleton_i_info = {}
    if '_x_singleton_i_lock' not in klass.__dict__:
        klass._x_singleton_i_lock = lock_factory()
    return klass


def mangle_cls_attr_map(cls_name: str, attr_map: typing.MutableMapping, do_update_func_name: bool = True):
    for attr_name, attr in tuple(attr_map.items()):
        if attr_name.startswith('__') is True and attr_name.endswith('__') is False:
            del attr_map[attr_name]
            new_attr_name = f'_{cls_name}{attr_name}'
            if do_update_func_name is True and isfunction(attr) is True:
                attr.__name__ = new_attr_name
            attr_map[new_attr_name] = attr
    return attr_map
