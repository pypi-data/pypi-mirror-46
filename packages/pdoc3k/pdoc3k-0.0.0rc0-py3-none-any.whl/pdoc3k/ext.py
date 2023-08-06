from .doc import Doc

__pdoc__ = {}

class External(Doc):
    """
    A representation of an external identifier. The textual
    representation is the same as an internal identifier, but without
    any context. (Usually this makes linking more difficult.)

    External identifiers are also used to represent something that is
    not exported but appears somewhere in the public interface (like
    the ancestor list of a class).
    """

    __pdoc__["External.docstring"] = \
        """
        An empty string. External identifiers do not have
        docstrings.
        """

    __pdoc__["External.module"] = \
        """
        Always `None`. External identifiers have no associated
        `pdoc.Module`.
        """

    __pdoc__["External.name"] = \
        """
        Always equivalent to `pdoc.External.refname` since external
        identifiers are always expressed in their fully qualified
        form.
        """

    def __init__(self, name):
        """
        Initializes an external identifier with `name`, where `name`
        should be a fully qualified name.
        """

        super().__init__(name, name, None, "")

    def extract_source(self):
        return []
