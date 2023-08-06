from importlib import import_module
from os import path
from pkgutil import iter_modules
import ast
import inspect
import sys
import traceback

import logbook

from .cls import BaseClass, Class, ExceptionClass
from .doc import ContainerDoc
from .error import DuplicateAliasError
from .func import ModuleFunction
from .util import extract_source, is_exported
from .var import ModuleVariable, ModuleVars

__pdoc__ = {}

class Module(ContainerDoc):
    """
    Representation of a module's documentation.
    """

    __pdoc__["Module.refname"] = \
        """
        The name of this module with respect to the context in which
        it was imported. It is always an absolute import path.
        """

    def __init__(self, module, parent, name, *, all_submodules=False):
        """
        Creates a `Module` documentation object given the actual
        module Python object.

        If `all_submodules` is `True`, then every submodule of this
        module that can be found will be included in the
        documentation, regardless of whether `__all__` contains it.
        """

        logbook.trace("initializing module {}", name)

        super().__init__(name.split(".")[-1], name, None, inspect.getdoc(module))

        self.parent = parent

        self._all_submodules = all_submodules

        self.pymod = module
        """
        Associated Python module object.
        """

        self.doc = {}
        """
        A mapping from identifier name to a documentation object.
        """

        self.refdoc = {}
        """
        The same as `pdoc.Module.doc`, but maps fully qualified
        identifier names to documentation objects.
        """

        self._aliases = {}

        try:
            src = inspect.getsource(self.pymod)
        except OSError:
            vardocs = {}
        else:
            vardocs = ModuleVars(ast.parse(src), self).search()

        self._declared_vars = vardocs.keys()

        logbook.trace("traversing public objects")

        for name, obj in self.__public_objs():
            try:
                # Skip any identifiers that already have docs.
                if not self.doc[name].is_empty():
                    continue
            except KeyError:
                pass

            # Functions and some weird builtins?, plus methods, classes,
            # modules and module level variables.
            if inspect.isroutine(obj):
                logbook.trace("adding function {}", name)
                self.doc[name] = ModuleFunction(name, self, obj)
            elif inspect.isclass(obj):
                if issubclass(obj, Exception):
                    logbook.trace("adding exception {}", name)
                    cls = ExceptionClass(name, self, obj)
                else:
                    logbook.trace("adding class {}", name)
                    cls = Class(name, self, obj)

                self.doc[name] = cls
                self._add_alias(name, obj)
            elif inspect.ismodule(obj):
                # Only document modules that are submodules or are forcefully
                # exported by __all__.
                if self.__is_exported(name, obj) or self.is_submodule(obj.__name__):
                    logbook.trace("adding submodule {}", name)
                    self.doc[name] = self.__new_submodule(name, obj)
                    self._add_alias(name, obj)
            else:
                try:
                    self.doc[name] = vardocs[name]
                except KeyError:
                    # Catch all for variables.
                    logbook.trace("adding variable {}", name)
                    self.doc[name] = ModuleVariable(name, self, "")

        self.is_package = self._traverse_package()

    def finalize(self):
        # Build the reference name dictionary.
        for basename, docobj in self.doc.items():
            self.refdoc[docobj.refname] = docobj

            if isinstance(docobj, BaseClass):
                for m in docobj.all_members():
                    self.refdoc[m.refname] = m

        try:
            overrides = self.pymod.__pdoc__
        except AttributeError:
            return

        # Finally look for more docstrings in the __pdoc__ override.
        for name, docstring in overrides.items():
            refname = "{}.{}".format(self.refname, name)

            if docstring is None:
                self.doc.pop(name, None)
                self.refdoc.pop(refname, None)
                continue

            try:
                dobj = self.refdoc[refname]
            except KeyError:
                raise ValueError("module doesn't contain {}".format(name))

            dobj.docstring = inspect.cleandoc(docstring)

    def lookup(self, name):
        try:
            name = self._aliases[name]
        except KeyError:
            pass

        return self.doc[name]

    def _traverse_package(self):
        try:
            # From https://docs.python.org/3/reference/import.html#packages:
            # "Specifically, any module that contains a __path__ attribute is considered a
            # package."
            pkgdir = self.pymod.__path__
        except AttributeError:
            logbook.debug("{} is not a package", self.refname)
            return False

        logbook.info("traversing package {}", self.refname)

        for _, root, _ in iter_modules(pkgdir):
            # Ignore if this module was already doc'd.
            if root in self.doc:
                continue

            # Ignore if it isn't exported, unless we've specifically
            # requested to document all submodules.
            if not self._submodule_exported(root):
                continue

            logbook.trace("visiting package module {}", root)

            fullname = "{}.{}".format(self.refname, root)

            try:
                m = import_module(fullname)
            except:
                logbook.warn("unable to import {}:", fullname)
                traceback.print_exc()
                continue

            self.doc[root] = self.__new_submodule(root, m)
            self._add_alias(root, m)

        return True

    def _submodule_exported(self, name):
        """
        Check if the given submodule name is public and exported from the current
        package.
        """

        return self._all_submodules and is_exported(name) or \
               self.__is_exported(name, self.pymod)

    def _add_alias(self, name, obj):
        basename = obj.__name__.split(".")[-1]

        if basename == name:
            return

        if basename in self._aliases:
            raise DuplicateAliasError(basename)

        self._aliases[basename] = name

    def extract_source(self):
        return extract_source(self.pymod)

    def is_public(self, name):
        """
        Returns `True` if and only if an identifier with name `name` is
        part of the public interface of this module. While the names
        of sub-modules are included, identifiers only exported by
        sub-modules are not checked.

        `name` should be a fully qualified name, e.g.,
        <code>pdoc.Module.is_public</code>.
        """

        return name in self.refdoc

    def variables(self):
        """
        Returns all documented module level variables in the module
        sorted alphabetically as a list of `pdoc.ModuleVariable`.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, ModuleVariable))

    def all_classes(self):
        return sorted(x for x in self.doc.values() if isinstance(x, BaseClass))

    def classes(self):
        """
        Returns all documented module level classes in the module
        sorted alphabetically as a list of `pdoc.Class`.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, Class))

    def exceptions(self):
        return sorted(x for x in self.doc.values() if isinstance(x, ExceptionClass))

    def functions(self):
        """
        Returns all documented module level functions in the module
        sorted alphabetically as a list of `pdoc.ModuleFunction`.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, ModuleFunction))

    def submodules(self):
        """
        Returns all documented sub-modules in the module sorted
        alphabetically as a list of `pdoc.Module`.
        """

        return sorted(x for x in self.doc.values() if isinstance(x, Module))

    def is_submodule(self, name):
        """
        Returns `True` if and only if `name` starts with the full
        import path of `self` and has length at least one greater than
        `len(self.refname)`.
        """

        return self.refname != name and name.startswith(self.refname)

    def __is_exported(self, name, module):
        """
        Returns `True` if and only if `pdoc` considers `name` to be
        a public identifier for this module where `name` was defined
        in the Python module `module`.

        If this module has an `__all__` attribute, then `name` is
        considered to be exported if and only if it is a member of
        this module's `__all__` list.

        If `__all__` is not set, then whether `name` is exported or
        not is heuristically determined. Firstly, if `name` starts
        with an underscore, it will not be considered exported.
        Secondly, if `name` was defined in a module other than this
        one, it will not be considered exported. In all other cases,
        `name` will be considered exported.
        """

        try:
            return name in self.pymod.__all__
        except AttributeError:
            pass

        if not is_exported(name):
            return False

        if module is None or self.pymod.__name__ != module.__name__:
            return name in self._declared_vars

        return True

    def __public_objs(self):
        """
        Returns a dictionary mapping a public identifier name to a
        Python object.
        """

        return ((name, obj) for name, obj in inspect.getmembers(self.pymod)
                     if self.__is_exported(name, inspect.getmodule(obj)))

    def __new_submodule(self, name, obj):
        """
        Create a new submodule documentation object for this `obj`,
        which must by a Python module object and pass along any
        settings in this module.
        """

        # Forcefully set the module name so that it is always the absolute
        # import path. We can't rely on `obj.__name__`, since it doesn't
        # necessarily correspond to the public exported name of the module.
        return Module(obj, self, "{}.{}".format(self.refname, name),
                      all_submodules=self._all_submodules)
