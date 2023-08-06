HTML_MODULE_SUFFIX = ".html"
"""
The suffix to use for module HTML files. By default, this is set to
`.m.html`, where the extra `.m` is used to differentiate a package's
`index.html` from a submodule called `index`.
"""

HTML_PACKAGE_NAME = "index{}".format(HTML_MODULE_SUFFIX)
"""
The file name to use for a package's `__init__.py` module.
"""
