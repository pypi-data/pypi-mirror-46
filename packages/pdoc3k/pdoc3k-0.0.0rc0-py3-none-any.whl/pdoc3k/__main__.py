#!/usr/bin/env python3

import argparse
import sys

from importlib_resources import read_text
from logbook import StderrHandler
import logbook

from . import DocTree, HtmlRender

LOG_FMT = "{record.level_name:>7} {record.time}: [{record.module}] {record.message}"

def main():
    args = argparse.ArgumentParser(
        description="Automatically generate API docs for Python modules.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    args.add_argument("modules", type=str, nargs="*",
       help="The Python module name. This may be an import path resolvable in "
            "the current environment, or a file path to a Python module or "
            "package.")
    args.add_argument("--version", action="store_true",
       help="Print the version of pdoc3k and exit.")
    args.add_argument("-v", "--verbose", action="count", default=0,
        help="increase logging verbosity (pass multiple times to increase further)")
    args.add_argument("-o", "--output-dir", type=str, default=".",
       help="The directory to output HTML files to. This option is ignored when "
            "outputting documentation as plain text.")
    args.add_argument("--no-source", action="store_true",
       help="When set, source code will not be viewable in the generated HTML. "
            "This can speed up the time required to document large modules.")
    args.add_argument("--latex", action="store_true",
        help="Enable LaTeX rendering via MathJax")
    args.add_argument("--all-submodules", action="store_true",
       help="When set, every submodule will be included, regardless of whether "
            "__all__ is set and contains the submodule.")
    args = args.parse_args()

    if args.version:
        print("pdoc3k v{}".format(read_text("pdoc3k", "version.txt").strip()))
        return

    if args.verbose == 0:
        level = logbook.INFO
    elif args.verbose == 1:
        level = logbook.DEBUG
    else:
        level = logbook.TRACE

    with StderrHandler(level=level, format_string=LOG_FMT).applicationbound():
        run(args)

def run(args):
    if not args.modules:
        logbook.warn("no modules specified")
        return

    # We close stdin because some modules, upon import, are not very polite
    # and block on stdin.
    try:
        sys.stdin.close()
    except:
        pass

    tree = DocTree()

    with tree.init_roots() as roots:
        for name in args.modules:
            logbook.info("adding {} to doc tree", name)
            roots.add(name, all_submodules=args.all_submodules)

    # HTML output depends on whether the module being documented is a package
    # or not. If not, then output is written to {MODULE_NAME}.html in
    # `html-dir`. If it is a package, then a directory called {MODULE_NAME}
    # is created, and output is written to {MODULE_NAME}/index.html.
    # Submodules are written to {MODULE_NAME}/{MODULE_NAME}.m.html and
    # subpackages are written to {MODULE_NAME}/{MODULE_NAME}/index.html. And
    # so on...
    logbook.info("rendering html to {}", args.output_dir)
    html = HtmlRender(tree, args.output_dir,
                      show_source_code=not args.no_source,
                      use_latex=args.latex)
    html.render()

if __name__ == "__main__":
    main()
