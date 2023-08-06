import ast

from .doc import Doc
from .util import is_exported

class Variable(Doc):
    def extract_source(self):
        return []

class ModuleVariable(Variable):
    """
    Representation of a variable's documentation. This includes
    module, class and instance variables.
    """

    def __init__(self, name, module, docstring):
        """
        Same as `pdoc.Doc.__init__`, except `cls` should be provided
        as a `pdoc.Class` object when this is a class or instance
        variable.
        """

        super().__init__(name, "{}.{}".format(module.refname, name), module, docstring)

        try:
            value = repr(getattr(self.module.pymod, name))
        except AttributeError:
            value = None

        self.value = value

class BaseClassVariable(Variable):
    def __init__(self, name, module, docstring, cls, value):
        super().__init__(name, "{}.{}".format(cls.refname, name), module, docstring)

        self.cls = cls
        """
        The `pdoc.Class` object if this is a class or instance
        variable. If not, this is None.
        """

        self.value = value

        self.inherits = None

class ClassVariable(BaseClassVariable):
    def __init__(self, name, module, docstring, cls):
        try:
            value = repr(getattr(cls.cls, name))
        except AttributeError:
            value = None

        super().__init__(name, module, docstring, cls, value)

class ClassProperty(BaseClassVariable):
    def __init__(self, name, module, docstring, cls):
        super().__init__(name, module, docstring, cls, None)

class ClassInitVariable(BaseClassVariable):
    def __init__(self, name, module, docstring, cls):
        super().__init__(name, module, docstring, cls, None)

class VarDocstrings:
    """
    Extracts variable docstrings given `tree` as the abstract syntax,
    `module` as a `pdoc.Module` containing `tree` and an option `cls`
    as a `pdoc.Class` corresponding to the tree. In particular, `cls`
    should be specified when extracting docstrings from a class or an
    `__init__` method. Finally, `init` should be `True` when searching
    the AST of an `__init__` method so that `_var_docstrings` will only
    accept variables starting with `self.` as instance variables.

    A dictionary mapping variable name to a `pdoc.ModuleVariable` object is
    returned.
    """

    def __init__(self, root, module):
        self._root = root
        self._module = module
        self._vars = {}

    def search(self):
        self._search(self._root)
        return self._vars

    def _search(self, tree):
        children = iter(ast.iter_child_nodes(tree))

        while True:
            try:
                child = next(children)
            except StopIteration:
                break

            self._search_node(child, children)

    def _search_node(self, child, children):
        while True:
            if isinstance(child, ast.Assign) and len(child.targets) == 1:
                if not self.include_node(child):
                    break

                name = self.var_name(child)

                if not self.include_var(name):
                    break

                child = next(children, None)

                if not self.is_docstring(child):
                    self._set_var(name, "")
                    continue

                self._set_var(name, self.extract_docstring(child))
            elif self.should_search(child):
                self._search(child)

            return

    def _set_var(self, name, docstring):
        self._vars[name] = self.create_var(name, docstring)

    @staticmethod
    def should_search(node):
        return isinstance(node, (
            ast.With,
            ast.AsyncWith,
            ast.If,
            ast.Try,
            ast.ExceptHandler,
        ))

    @staticmethod
    def is_docstring(node):
        return isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)

    @staticmethod
    def extract_docstring(node):
        return node.value.s

    def include_var(self, name):
        return is_exported(name)

    def include_node(self, node):
        return isinstance(node.targets[0], ast.Name)

    def var_name(self, node):
        return node.targets[0].id

class ModuleVars(VarDocstrings):
    def __init__(self, *args):
        super().__init__(*args)

        try:
            self._all = self.module.__all__
        except AttributeError:
            self._all = []

    def include_var(self, name):
        return super().include_var(name) and name not in self._all

    def create_var(self, name, docstring):
        return ModuleVariable(name, self._module, docstring)

class ClassVars(VarDocstrings):
    def __init__(self, cls, *args):
        super().__init__(*args)

        self._cls = cls

    def create_var(self, name, docstring):
        return ClassVariable(name, self._module, docstring, self._cls)

class ClassInitVars(ClassVars):
    def include_node(self, node):
        return isinstance(node.targets[0], ast.Attribute) and \
               isinstance(node.targets[0].value, ast.Name) and \
               node.targets[0].value.id == "self"

    def var_name(self, node):
        return node.targets[0].attr

    def create_var(self, name, docstring):
        return ClassInitVariable(name, self._module, docstring, self._cls)
