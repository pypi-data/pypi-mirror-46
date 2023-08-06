from inspect import getdoc, iscoroutinefunction, signature, Signature, formatannotation
import inspect

from .doc import Doc
from .util import extract_source

class Function(Doc):
    """
    Representation of documentation for a Python function or method.
    """

    def __init__(self, name, refname, module, func):
        """
        Same as `pdoc.Doc.__init__`, except `func_obj` must be a
        Python function object. The docstring is gathered automatically.
        """

        super().__init__(name, refname, module, getdoc(func))

        self.func = func
        """
        The Python function object.
        """

    def extract_source(self):
        return extract_source(self.func)

    def funcdef(self):
        """
        Generates the string of keywords used to define the function, for example `def` or
        `async def`.
        """

        if self._is_async():
            return "async def"
        else:
            return "def"

    def _is_async(self):
        """
        Returns whether this function is asynchronous, either as a coroutine or an async
        generator.
        """

        try:
            # Both of these are required because coroutines aren't classified as async
            # generators and vice versa.
            return inspect.iscoroutinefunction(self.func) or \
                   inspect.isasyncgenfunction(self.func)
        except AttributeError:
            return False

    def spec(self):
        """
        Returns a nicely formatted spec of the function's parameter
        list as a string. This includes argument lists, keyword
        arguments and default values.
        """

        try:
            sig = signature(self.func)
        except ValueError:
            return "...", None

        try:
            ret = sig.return_annotation
        except AttributeError:
            ret = Signature.empty
        else:
            sig = sig.replace(return_annotation=Signature.empty)

        # Strip off opening and closing parens.
        params = str(sig)[1:-1]

        if ret is Signature.empty:
            ret = None
        else:
            ret = formatannotation(ret)

        return params, ret

    def __lt__(self, other):
        return self.name < other.name

class ModuleFunction(Function):
    def __init__(self, name, module, func):
        super().__init__(name, "{}.{}".format(module.refname, name), module, func)

class ClassFunction(Function):
    def __init__(self, name, module, cls, func):
        super().__init__(name, "{}.{}".format(cls.refname, name), module, func)

        self.cls = cls
        """
        The `pdoc.Class` documentation object if this is a method. If
        not, this is None.
        """

        self.inherits = None

class StaticMethod(ClassFunction):
    pass

class ClassMethod(ClassFunction):
    pass

class InstanceMethod(ClassFunction):
    pass
