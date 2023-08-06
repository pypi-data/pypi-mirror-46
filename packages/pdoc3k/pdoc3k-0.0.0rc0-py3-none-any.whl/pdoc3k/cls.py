from inspect import getdoc, getsource, isfunction, isbuiltin, isroutine, getmembers
import ast

import logbook

from .doc import ContainerDoc
from .func import InstanceMethod, StaticMethod, ClassMethod
from .util import is_exported, extract_source
from .var import ClassVariable, ClassInitVariable, ClassProperty, ClassVars, \
        ClassInitVars

class BaseClass(ContainerDoc):
    """
    Representation of a class's documentation.
    """

    def __init__(self, name, module, pyclass):
        """
        Same as `pdoc.Doc.__init__`, except `pyclass` must be a
        Python class object. The docstring is gathered automatically.
        """

        logbook.trace("initializing class {}", name)

        super().__init__(name,
            "{}.{}".format(module.refname, pyclass.__name__),
            module, getdoc(pyclass))

        self.pyclass = pyclass
        """
        The class Python object.
        """

        # First try and find docstrings for class variables.
        # Then move on to finding docstrings for instance variables.
        # This must be optional, since not all modules have source
        # code available.
        try:
            src = getsource(self.pyclass)
        except OSError:
            doc = {}
            doc_init = {}
        else:
            doc, doc_init = self._search_vars(src)

        self.doc = doc
        """
        A mapping from identifier name to a `pdoc.Doc` objects.
        """

        self.doc_init = doc_init
        """
        A special version of `pdoc.Class.doc` that contains
        documentation for instance variables found in the `__init__`
        method.
        """

        logbook.trace("traversing public members")

        # Convert the public Python objects to documentation objects.
        for name, obj in self.__public_objs():
            try:
                # Skip any identifiers that already have docs.
                if not self.doc[name].is_empty():
                    continue
            except KeyError:
                pass

            if name in self.doc_init:
                # Let instance members override class members.
                continue

            try:
                desc = self.pyclass.__dict__[name]
            except KeyError:
                desc = obj

            if isinstance(desc, classmethod):
                logbook.trace("adding classmethod {}", name)
                self.doc[name] = ClassMethod(name, self.module, self, obj.__func__)
            elif isinstance(desc, staticmethod):
                logbook.trace("adding staticmethod {}", name)
                self.doc[name] = StaticMethod(name, self.module, self, obj)
            elif isinstance(obj, property):
                logbook.trace("adding property {}", name)
                self.doc[name] = ClassProperty(name, self.module, getdoc(obj), self)
            elif isroutine(desc):
                logbook.trace("adding instance method {}", name)
                self.doc[name] = InstanceMethod(name, self.module, self, obj)
            elif not isbuiltin(obj) and not isroutine(obj):
                try:
                    slots = self.pyclass.__slots__
                except AttributeError:
                    initvar = False
                else:
                    initvar = name in slots

                if initvar:
                    logbook.trace("adding initvar {}", name)
                    self.doc_init[name] = ClassInitVariable(name, self.module, "", self)
                else:
                    logbook.trace("adding var {}", name)
                    self.doc[name] = ClassVariable(name, self.module, "", self)

        self.mro = None

    def extract_source(self):
        return extract_source(self.pyclass)

    def lookup(self, name):
        try:
            return self.doc_init[name]
        except KeyError:
            return self.doc[name]

    def class_variables(self):
        """
        Returns all documented class variables in the class, sorted
        alphabetically as a list of `pdoc.ModuleVariable`.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, ClassVariable))

    def instance_variables(self):
        """
        Returns all instance variables in the class, sorted
        alphabetically as a list of `pdoc.ModuleVariable`. Instance variables
        are attributes of `self` defined in a class's `__init__`
        method.
        """

        return sorted(self.doc_init.values())

    def properties(self):
        return sorted(x for x in self.doc.values() if isinstance(x, ClassProperty))

    def methods(self):
        """
        Returns all documented methods as `pdoc.InstanceMethod` objects in
        the class, sorted alphabetically with `__init__` always coming
        first.

        Unfortunately, this also includes class methods.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, InstanceMethod))

    def functions(self):
        """
        Returns all documented static functions as `pdoc.StaticMethod`
        objects in the class, sorted alphabetically.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, StaticMethod))

    def class_methods(self):
        return sorted(x for x in self.doc.values() if isinstance(x, ClassMethod))

    def all_members(self):
        yield from self.doc.values()
        yield from self.doc_init.values()

    def _search_vars(self, src):
        tree = ast.parse(src).body[0]

        doc = ClassVars(self, tree, self.module).search()
        doc_init = self._search_init_vars(tree.body)

        return doc, doc_init

    def _search_init_vars(self, tree):
        for node in tree:
            if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)) and \
                    node.name == "__init__":
                return ClassInitVars(self, node, self.module).search()

        return {}

    def finalize(self, mro):
        logbook.trace("finalizing class {}", self.name)

        self.mro = mro

        self._fill_inheritance()
        self._remove_dups()

    def _fill_inheritance(self):
        """
        Traverses this class's ancestor list and attempts to fill in
        missing documentation from its ancestor's documentation.

        The first pass connects variables, methods and functions with
        their inherited couterparts. (The templates will decide how to
        display docstrings.) The second pass attempts to add instance
        variables to this class that were only explicitly declared in
        a parent class. This second pass is necessary since instance
        variables are only discoverable by traversing the abstract
        syntax tree.
        """

        mro = [c for c in self.mro if isinstance(c, BaseClass)]
        mro_doc = [c.doc for c in mro]
        mro_init = [c.doc_init for c in mro]

        for target in self.doc_init.values():
            try:
                target.inherits = _search_inheritance(mro_init, target)
            except _NoInheritanceError:
                pass

        for target in self.doc.values():
            try:
                target.inherits = _search_inheritance(mro_doc, target)
            except _NoInheritanceError:
                pass

        for cls in mro:
            for name, val in cls.doc_init.items():
                if name in self.doc_init:
                    continue

                var = ClassVariable(val.name, self.module, val.docstring, self)
                var.inherits = val

                self.doc_init[name] = var

    def _remove_dups(self):
        # Remove duplicate variables.
        for name in self.doc_init.keys():
            try:
                del self.doc[name]
            except KeyError:
                pass

    def __public_objs(self):
        """
        Returns a dictionary mapping a public identifier name to a
        Python object. This counts the `__init__` method as being
        public.
        """

        _pdoc = getattr(self.module.pymod, "__pdoc__", {})

        def forced_out(name):
            return _pdoc.get("{}.{}".format(self.name, name), False) is None

        def exported(name):
            exported = name == "__init__" or is_exported(name)
            return not forced_out(name) and exported

        return ((n, o) for n, o in getmembers(self.pyclass) if exported(n))

class Class(BaseClass):
    pass

class ExceptionClass(BaseClass):
    pass

def _search_inheritance(groups, target):
    for group in groups:
        try:
            docobj = group[target.name]
        except KeyError:
            continue

        if isinstance(target, type(docobj)):
            return docobj

    raise _NoInheritanceError()

class _NoInheritanceError(ValueError):
    pass

