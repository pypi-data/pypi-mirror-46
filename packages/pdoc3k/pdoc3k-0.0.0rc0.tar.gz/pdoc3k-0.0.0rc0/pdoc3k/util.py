from inspect import getsourcelines

def extract_source(obj):
    """
    Returns the source code of the Python object `obj` as a list of
    lines. This tries to extract the source from the special
    `__wrapped__` attribute if it exists. Otherwise, it falls back
    to `inspect.getsourcelines`.

    If neither works, then the empty list is returned.
    """

    try:
        return getsourcelines(obj)[0]
    except (OSError, TypeError):
        return []

def is_exported(ident_name):
    """
    Returns `True` if `ident_name` matches the export criteria for an
    identifier name.

    This should not be used by clients. Instead, use
    `pdoc.Module.is_public`.
    """

    return not ident_name.startswith("_")
