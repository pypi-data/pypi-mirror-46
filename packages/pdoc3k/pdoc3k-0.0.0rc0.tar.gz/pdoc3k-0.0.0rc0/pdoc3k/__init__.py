"""
Module pdoc provides types and functions for accessing the public
documentation of a Python module. This includes modules (and
sub-modules), functions, classes and module, class and instance
variables.  Docstrings are taken from modules, functions and classes
using the special `__doc__` attribute. Docstrings for variables are
extracted by examining the module's abstract syntax tree.

The public interface of a module is determined through one of two
ways. If `__all__` is defined in the module, then all identifiers in
that list will be considered public. No other identifiers will be
considered as public. Conversely, if `__all__` is not defined, then
`pdoc` will heuristically determine the public interface. There are
three rules that are applied to each identifier in the module:

1. If the name starts with an underscore, it is **not** public.
2. If the name is defined in a different module, it is **not** public.
3. If the name refers to an immediate sub-module, then it is public.

Once documentation for a module is created with `pdoc.Module`, it
can be output as either HTML or plain text using the covenience
functions `pdoc.html` and `pdoc.text`, or the corresponding methods
`pdoc.Module.html` and `pdoc.Module.text`.

Compatibility
-------------
`pdoc` has been tested on Python 2.6, 2.7 and 3.3. It seems to work
on all three.

Contributing
------------
`pdoc` [is on GitHub](https://github.com/BurntSushi/pdoc). Pull
requests and bug reports are welcome.

Linking to other identifiers
----------------------------
In your documentation, you may link to other identifiers in
your module or submodules. Linking is automatically done for
you whenever you surround an identifier with a back quote
(grave). The identifier name must be fully qualified. For
example, <code>\`pdoc.Doc.docstring\`</code> is correct while
<code>\`Doc.docstring\`</code> is incorrect.

Where does pdoc get documentation from?
---------------------------------------
Broadly speaking, `pdoc` gets everything you see from introspecting the
module. This includes words describing a particular module, class,
function or variable. While `pdoc` does some analysis on the source
code of a module, importing the module itself is necessary to use
Python's introspection features.

In Python, objects like modules, functions, classes and methods have
a special attribute named `__doc__` which contains that object's
*docstring*.  The docstring comes from a special placement of a string
in your source code.  For example, the following code shows how to
define a function with a docstring and access the contents of that
docstring:

    #!python
    >>> def test():
    ...     '''This is a docstring.'''
    ...     pass
    ...
    >>> test.__doc__
    'This is a docstring.'

Something similar can be done for classes and modules too. For classes,
the docstring should come on the line immediately following `class
...`. For modules, the docstring should start on the first line of
the file. These docstrings are what you see for each module, class,
function and method listed in the documentation produced by `pdoc`.

The above just about covers *standard* uses of docstrings in Python.
`pdoc` extends the above in a few important ways.

### Special docstring conventions used by `pdoc`

**Firstly**, docstrings can be inherited. Consider the following code
sample:

    #!python
    >>> class A (object):
    ...     def test():
    ...         '''Docstring for A.'''
    ...
    >>> class B (A):
    ...     def test():
    ...         pass
    ...
    >>> print(A.test.__doc__)
    Docstring for A.
    >>> print(B.test.__doc__)
    None

In Python, the docstring for `B.test` is empty, even though one was
defined in `A.test`. If `pdoc` generates documentation for the above
code, then it will automatically attach the docstring for `A.test` to
`B.test` only if `B.test` does not have a docstring. In the default
HTML output, an inherited docstring is grey.

**Secondly**, docstrings can be attached to variables, which includes
module (or global) variables, class variables and instance variables.
Python by itself [does not allow docstrings to be attached to
variables](http://www.python.org/dev/peps/pep-0224). For example:

    #!python
    variable = "SomeValue"
    '''Docstring for variable.'''

The resulting `variable` will have no `__doc__` attribute. To
compensate, `pdoc` will read the source code when it's available to
infer a connection between a variable and a docstring. The connection
is only made when an assignment statement is followed by a docstring.

Something similar is done for instance variables as well. By
convention, instance variables are initialized in a class's `__init__`
method.  Therefore, `pdoc` adheres to that convention and looks for
docstrings of variables like so:

    #!python
    def __init__(self):
        self.variable = "SomeValue"
        '''Docstring for instance variable.'''

Note that `pdoc` only considers attributes defined on `self` as
instance variables.

Class and instance variables can also have inherited docstrings.

**Thirdly and finally**, docstrings can be overridden with a special
`__pdoc__` dictionary that `pdoc` inspects if it exists. The keys of
`__pdoc__` should be identifiers within the scope of the module. (In
the case of an instance variable `self.variable` for class `A`, its
module identifier would be `A.variable`.) The values of `__pdoc__`
should be docstrings.

This particular feature is useful when there's no feasible way of
attaching a docstring to something. A good example of this is a
[namedtuple](http://goo.gl/akfXJ9):

    #!python
    __pdoc__ = {}

    Table = namedtuple('Table', ['types', 'names', 'rows'])
    __pdoc__['Table.types'] = 'Types for each column in the table.'
    __pdoc__['Table.names'] = 'The names of each column in the table.'
    __pdoc__['Table.rows'] = 'Lists corresponding to each row in the table.'

`pdoc` will then show `Table` as a class with documentation for the
`types`, `names` and `rows` members.

Note that assignments to `__pdoc__` need to placed where they'll be
executed when the module is imported. For example, at the top level
of a module or in the definition of a class.

If `__pdoc__[key] = None`, then `key` will not be included in the
public interface of the module.

License
-------
`pdoc` is in the public domain via the
[UNLICENSE](http://unlicense.org).
"""

from contextlib import contextmanager
from importlib import import_module
from importlib.machinery import SourceFileLoader
from inspect import getmro
from os import path
from pathlib import Path
import os

from importlib_resources import path as open_path
from mako.exceptions import TopLevelLookupException
from mako.lookup import TemplateLookup
from mako.runtime import Context
import logbook

from .cls import BaseClass
from .consts import HTML_MODULE_SUFFIX, HTML_PACKAGE_NAME
from .doc import ContainerDoc
from .error import UnknownRootError, ResolveError
from .ext import External
from .module import Module
from . import templates

__pdoc__ = {}

class DocTreeRoots:
    __pdoc__["DocTreeRoots.__init__"] = None

    def __init__(self, tree):
        self._tree = tree

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._tree._finalize()

    def add(self, target, *, all_submodules=False):
        module, name = _root_module(target)
        root = Module(module, None, name, all_submodules=all_submodules)

        self._tree._roots[root.refname] = root

class DocTree:
    def __init__(self):
        self._roots = {}

    def init_roots(self) -> DocTreeRoots:
        return DocTreeRoots(self)

    def __iter__(self):
        return iter(self._roots.values())

    def _finalize(self):
        logbook.trace("finalizing doc tree")
        for root in self:
            self._finalize_mod(root)

    def _finalize_mod(self, mod):
        for submod in mod.submodules():
            self._finalize_mod(submod)

        for cls in mod.all_classes():
            self._finalize_cls(cls)

        mod.finalize()

    def _finalize_cls(self, cls):
        if cls.mro is not None:
            return

        mro = list(self._resolve_mro(cls))

        for obj in mro:
            if isinstance(obj, BaseClass):
                self._finalize_cls(obj)

        cls.finalize(mro)

    def resolve_name(self, refname) -> Module:
        return self.resolve_path(refname.split("."))

    def resolve_path(self, path) -> Module:
        root = path[0]

        try:
            cur = self._roots[root]
        except KeyError:
            raise UnknownRootError()

        for seg in path[1:]:
            if not isinstance(cur, ContainerDoc):
                raise ResolveError()

            try:
                cur = cur.lookup(seg)
            except LookupError:
                raise ResolveError()

        return cur

    def _resolve_mro(self, cls):
        for scls in getmro(cls.pyclass)[1:]:
            refname = "{}.{}".format(scls.__module__, scls.__name__)

            try:
                yield self.resolve_name(refname)
            except UnknownRootError:
                yield External(refname)
            except ResolveError:
                continue

class HtmlRender:
    def __init__(self, tree, output_dir, **kwargs):
        """
        Returns the documentation for this module as
        self-contained HTML.

        If `source` is `True`, then source code will be retrieved for
        every Python object whenever possible. This can dramatically
        decrease performance when documenting large modules.

        `kwargs` is passed to the `mako` render function.
        """

        self._tree = tree
        self._output_dir = Path(output_dir)
        self._kwargs = kwargs
        self._template = None

    def render(self):
        with self._open_templates():
            for mod in self._tree:
                self._output_mod(mod)

    @contextmanager
    def _open_templates(self):
        with open_path(templates, ".") as tdir:
            lookup = TemplateLookup(
                    directories=[str(tdir)],
                    cache_args={
                        "cached": True,
                        "cache_type": "memory",
                    },
                    input_encoding="utf-8",
            )

            self._template = lookup.get_template("/html.mako")

            yield

    def _output_mod(self, mod):
        path = self._module_file(mod)
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with path.open("w") as f:
                self._render_mod(mod, f)
        except Exception:
            try:
                path.unlink()
            except NameError:
                pass

            raise

        for submodule in mod.submodules():
            self._output_mod(submodule)

    def _render_mod(self, mod, stream):
        return self._template.render_context(Context(stream,
            module=mod,
            tree=self._tree,
            **self._kwargs
        ))

    def _module_file(self, mod):
        mbase = self._output_dir.joinpath(*mod.refname.split("."))

        if mod.is_package:
            return mbase.joinpath(HTML_PACKAGE_NAME)
        else:
            return mbase.with_name("{}{}".format(mbase.name, HTML_MODULE_SUFFIX))

def _root_module(target):
    # Try to do a real import first. I think it's better to prefer
    # import paths over files. If a file is really necessary, then
    # specify the absolute path, which is guaranteed not to be a
    # Python import path.
    try:
        pymod = import_module(target)
    except (ImportError, TypeError):
        pass
    else:
        return pymod, pymod.__name__

    # Get the module that we're documenting. Accommodate for import paths,
    # files and directories.
    rp = path.realpath(target)

    if not path.exists(rp):
        raise RuntimeError("unknown module {}".format(target))

    name = path.basename(rp)

    if path.isdir(rp):
        fp = path.join(rp, "__init__.py")
        module = SourceFileLoader(name, fp).load_module()
        module.__path__ = [rp]
    else:
        name, _ = path.splitext(name)
        module = SourceFileLoader(name, rp).load_module()

    return module, name
