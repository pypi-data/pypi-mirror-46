class DuplicateAliasError(RuntimeError):
    def __init__(self, name):
        super().__init__("alias '{}' already exists".format(name))

class ResolveError(RuntimeError):
    pass

class UnknownRootError(ResolveError):
    pass
