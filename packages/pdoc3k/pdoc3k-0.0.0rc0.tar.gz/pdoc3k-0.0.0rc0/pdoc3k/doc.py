from inspect import cleandoc

class Doc:
    """
    A base class for all documentation objects.

    A documentation object corresponds to *something* in a Python module
    that has a docstring associated with it. Typically, this only includes
    modules, classes, functions and methods. However, `pdoc` adds support
    for extracting docstrings from the abstract syntax tree, which means
    that variables (module, class or instance) are supported too.

    A special type of documentation object `pdoc.External` is used to
    represent identifiers that are not part of the public interface of
    a module. (The name "External" is a bit of a misnomer, since it can
    also correspond to unexported members of the module, particularly in
    a class's ancestor list.)
    """

    def __init__(self, name, refname, module, docstring):
        """
        Initializes a documentation object, where `name` is the public
        identifier name, `module` is a `pdoc.Module` object, and
        `docstring` is a string containing the docstring for `name`.
        """

        self.module = module
        """
        The module documentation object that this object was defined
        in.
        """

        self.name = name
        """
        The identifier name for this object.
        """

        self.refname = refname
        """
        An appropriate reference name for this documentation
        object. Usually this is its fully qualified path.
        """

        self.docstring = cleandoc(docstring or "").strip()
        """
        The docstring for this object. It has already been cleaned
        by `inspect.cleandoc`.
        """

    def extract_source(self):
        """
        Extracts the source code of the current object as a list of lines.

        If the source couldn't be extracted, then an empty list is returned.
        """

        raise NotImplementedError

    def __lt__(self, other):
        return self.name < other.name

    def is_empty(self):
        """
        Returns true if the docstring for this object is empty.
        """

        return len(self.docstring) == 0

class ContainerDoc(Doc):
    def lookup(self, name):
        raise NotImplementedError
