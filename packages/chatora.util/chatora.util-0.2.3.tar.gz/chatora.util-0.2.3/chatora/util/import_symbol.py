__all__ = (
    'maybe_resolve_obj_from_symbol_path',
    'maybe_resolve_symbol_path_from_obj',
    'normalize_symbol_path',
)


def maybe_resolve_obj_from_symbol_path(symbol_path_or_obj):
    """ Import the symbol defined by the specified symbol path.

    Examples
    --------

    import_symbol('tarfile:TarFile') -> TarFile
    import_symbol('tarfile:TarFile.open') -> TarFile.open

    To allow compatibility with old-school traits symbol names we also allow
    all-dotted paths, but in this case you can only import top-level names
    from the module.

    import_symbol('tarfile.TarFile') -> TarFile

    """

    if isinstance(symbol_path_or_obj, str) is False:
        return symbol_path_or_obj
    elif ':' in symbol_path_or_obj:
        module_name, symbol_name = symbol_path_or_obj.split(':')
        return eval(
            symbol_name,
            __import__(module_name, {}, {}, [symbol_name], 0).__dict__,
        )
    elif '.' in symbol_path_or_obj:
        *components, symbol_name = symbol_path_or_obj.split('.')
        return getattr(
            __import__('.'.join(components[:-1]), {}, {}, [symbol_name], 0),
            symbol_name,
        )


def maybe_resolve_symbol_path_from_obj(obj_or_symbol_path):
    return normalize_symbol_path(
        symbol_path=obj_or_symbol_path,
    ) if isinstance(obj_or_symbol_path, str) is True \
        else f'{obj_or_symbol_path.__module__}:{obj_or_symbol_path.__name__}'


def normalize_symbol_path(symbol_path):
    return symbol_path if ':' in symbol_path else ':'.join(symbol_path.rsplit('.', 1))
