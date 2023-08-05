__all__ = (
    '_BaseMarker',
    '_Marker',
    '_Null',
    '_Undefined',
    'MARKER',
    'NULL',
    'UNDEFINED',
    'NOT_FOUND',
)


class _BaseMarker:

    __slots__ = ()

    def __reduce__(self):
        # when unpickled, refers to the marker (singleton)
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
        return True


class _Marker(_BaseMarker):

    __name__ = 'MARKER'
    __slots__ = ()


MARKER: _Marker = _Marker()


class _Null(_BaseMarker):

    __name__ = 'NULL'
    __slots__ = ()

    def __bool__(self):
        return False


NULL: _Null = _Null()


class _Undefined(_Null):

    __name__ = 'UNDEFINED'
    __slots__ = ()


UNDEFINED: _Undefined = _Undefined()


class _NotFound(_Null):

    __name__ = 'NOT_FOUND'
    __slots__ = ()


NOT_FOUND: _NotFound = _NotFound()
