<%
from os.path import relpath
import re
import sys

import markdown

try:
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import Python3Lexer
except ImportError:
    use_pygments = False
else:
    use_pygments = True

from pdoc3k.cls import BaseClass
from pdoc3k.consts import HTML_MODULE_SUFFIX
from pdoc3k.error import ResolveError, UnknownRootError
from pdoc3k.ext import External
from pdoc3k.func import ClassFunction, ModuleFunction
from pdoc3k.module import Module
from pdoc3k.var import BaseClassVariable, ModuleVariable
import pdoc3k

def clean_source_lines(lines):
    """
    Cleans the source code so that pygments can render it well.

    Returns one string with all of the source code.
    """

    indent = 0

    for line in lines:
        trimmed = len(line.lstrip())

        if trimmed > 0:
            indent = len(line) - trimmed
            break

    lines = "".join(line[indent:] for line in lines)

    if not use_pygments:    # :-(
        return "<pre><code>{}</code></pre>".format(lines)

    pylex = Python3Lexer()
    htmlform = HtmlFormatter(cssclass="codehilite")

    return highlight(lines, pylex, htmlform)

def mark(s, d):
    s, _ = re.subn("\b\n\b", " ", s)
    s, _ = re.subn("`[^`]+`", lambda m: linkify(m, d), s)

    return markdown.markdown(s, extensions=[
        "markdown.extensions.fenced_code",
        "markdown.extensions.codehilite(linenums=False)",
        "markdown.extensions.toc(marker=None)",
    ])

def linkify(match, d):
    matched = match.group(0)
    ident = matched[1:-1]

    try:
        return "[`{}`]({})".format(ident, lookup(ident))
    except ResolveError:
        pass

    url = fuzzy_link(ident, d)

    if url is not None:
        return url

    return matched

def glimpse(s, length=100):
    s = s.split("\n")[0]

    if len(s) < length:
        return s

    return "{}...".format(s[:length])

def rel_link(src, dst):
    src = "/".join(src.refname.split("."))
    dst = "/".join(dst.refname.split("."))

    return relpath(dst, src)

def full_link(dst):
    if isinstance(dst, Module):
        dstmod = dst
        hash = ""
    else:
        dstmod = dst.module
        hash = "#{}".format(dst.refname)

    if module == dstmod:
        return hash

    if dstmod.is_package:
        suffix = "/"
    else:
        suffix = HTML_MODULE_SUFFIX

    if module.is_package:
        srcmod = module
    else:
        srcmod = module.parent

    link = rel_link(srcmod, dstmod)

    return "{}{}{}".format(link, suffix, hash)

def obj_url(dst):
    if isinstance(dst, External):
        return None
    else:
        return full_link(dst)

def ref_url(ident, ref):
    return "[`{}`]({})".format(ident, obj_url(ref))

def fuzzy_link(ident, d):
    if isinstance(d, BaseClass):
        try:
            return ref_url(ident, d.doc_init[ident])
        except KeyError:
            pass

        try:
            return ref_url(ident, d.doc[ident])
        except KeyError:
            pass

        return fuzzy_link(ident, d.module)

    if isinstance(d, Module):
        try:
            return ref_url(ident, d.doc[ident])
        except KeyError:
            return None

    if isinstance(d, (BaseClassVariable, ClassFunction)):
        return fuzzy_link(ident, d.cls) or fuzzy_link(ident, d.module)

    if isinstance(d, (ModuleVariable, ModuleFunction)):
        return fuzzy_link(ident, d.module)

    return None

def lookup(refname):
    """
    Given a fully qualified identifier name, return its refname
    with respect to the current module and a value for a `href`
    attribute. If `refname` is not in the public interface of
    this module or its submodules, then `None` is returned for
    both return values. (Unless this module has enabled external
    linking.)

    In particular, this takes into account sub-modules and external
    identifiers. If `refname` is in the public API of the current
    module, then a local anchor link is given. If `refname` is in the
    public API of a sub-module, then a link to a different page with
    the appropriate anchor is given. Otherwise, `refname` is
    considered external and no link is used.
    """

    return obj_url(tree.resolve_name(refname))

def lookupret(retname):
    try:
        return tree.resolve_name(retname)
    except UnknownRootError:
        return External(retname)

def breadcrumbs(modname):
    parts = modname.split(".")

    if len(parts) == 1:
        yield modname, "", ""
        return

    up = len(parts) - 2

    for idx, part in enumerate(parts[:up]):
        yield part, "../" * (up - idx), "."

    if module.is_package:
        path = "../"
    else:
        path = "."

    yield parts[-2], path, "."
    yield parts[-1], "", ""
%>

<%def name="ident(s)">\
<span class="ident">${s}</span>\
</%def>

<%def name="obj_link(obj, *, force_short=False)">\
<%
    name = obj.name if force_short or module.is_public(obj.refname) else obj.refname
    url = obj_url(obj)
%>\
% if url is None:
${name}\
% else:
<a href="${url}" title="${obj.refname}">${name}</a>\
% endif
</%def>

<%def name="show_source(d)">
    % if show_source_code:
    ${source_container(d.extract_source())}
    % endif
</%def>

<%def name="source_container(src)">
    % if src:
    <div class="sourcecontainer">
        <a href="#" class="sourcebutton">
            Source <span class="expandicon"></span>
        </a>
        <div class="source hidden">
            ${clean_source_lines(src)}
        </div>
    </div>
    % endif
</%def>

<%def name="desc(d, limit)">
    <%call expr="show_docstring(d, d.docstring, limit)" args="content">
        <div class="desc">${content}</div>
    </%call>
</%def>

<%def name="show_desc(d)">
    ${desc(d, None)}
    ${show_source(d)}
</%def>

<%def name="show_member_desc(d, limit=None)">
    <%
    inherits = d.inherits and (len(d.docstring) == 0 or d.docstring == d.inherits.docstring)
    %>
    % if inherits:
        <%call expr="show_docstring(d, d.inherits.docstring, limit)" args="content">
            <div class="desc inherited">${content}</div>
        </%call>
    % else:
        ${desc(d, limit)}
    % endif
    ${show_source(d)}
</%def>

<%def name="show_docstring(d, docstring, limit)">
    <%
    if limit is not None:
        docstring = glimpse(docstring, limit)
    %>
    % if docstring:
        ${caller.body(content=mark(docstring, d))}
    % endif
</%def>

<%def name="show_inheritance(d)">
    % if d.inherits is not None:
        <p class="inheritance">
         <strong title="Inherited from">⤷</strong>
         <code>${obj_link(d.inherits.cls)}.${obj_link(d.inherits, force_short=True)}</code>
        </p>
    % endif
</%def>

<%def name="name_container(obj)">
    <a href="#${obj.refname}" id="${obj.refname}" class="name">
        ${caller.body()}
    </a>
</%def>

<%def name="ident_name(x, ty)">
    <%call expr="name_container(x)">
        <span class="type">${ty}</span> ${ident(x.name)}
    </%call>
</%def>

<%def name="show_var(v)">
    <%call expr="name_container(v)">
        ${ident(v.name)}<span class="assign"> = ${show_value(v.value)}</span>
    </%call>
</%def>

<%def name="show_value(val)">
    % if val is None:
        &lt;⋯&gt;
    % else:
        ${glimpse(val, 50) | h}
    % endif
</%def>

<%def name="func_container(f)">
    <% params, ret = f.spec() %>
    <div class="item">
        <a href="#${f.refname}" class="name" id="${f.refname}">
            <div class="funcdef">
                <div class="funcinit">
                    <div class="funcname">
                        <span class="type">${f.funcdef()}</span>
                        ${ident(f.name)}(
                    </div>
                    <div class="funcargs">${params | h})</div>
                </div>
                % if ret is not None:
                <% retobj = lookupret(ret) %>
                <div class="funcret">
                    &nbsp;-&gt; ${obj_link(retobj)}
                </div>
                % endif
            </div>
        </a>
        ${caller.body()}
    </div>
</%def>

<%def name="show_func(f)">
    <%call expr="func_container(f)">
        ${show_desc(f)}
    </%call>
</%def>

<%def name="show_class_func(f)">
    <%call expr="func_container(f)">
        ${show_inheritance(f)}
        ${show_member_desc(f)}
    </%call>
</%def>

<%def name="show_class(c)">
    <%
    class_vars = c.class_variables()
    smethods = c.functions()
    cmethods = c.class_methods()
    inst_vars = c.instance_variables()
    properties = c.properties()
    methods = c.methods()
    %>
    <div class="item">
        ${ident_name(c, "class")}
        ${show_desc(c)}

        <div class="class">
            <h3 title="Listed in Method Resolution Order">Ancestors</h3>
            <ul class="ancestors">
            % for cls in c.mro:
                <li>${obj_link(cls)}</li>
            % endfor
            </ul>
            % if class_vars:
                <h3>Class variables</h3>
                % for v in class_vars:
                    <div class="item">
                    ${show_var(v)}
                    ${show_inheritance(v)}
                    ${show_member_desc(v)}
                    </div>
                % endfor
            % endif
            % if smethods:
                <h3 title="Methods with @staticmethod">Static methods</h3>
                % for f in smethods:
                    ${show_class_func(f)}
                % endfor
            % endif
            % if cmethods:
                <h3 title="Methods with @classmethod">Class methods</h3>
                % for f in cmethods:
                    ${show_class_func(f)}
                % endfor
            % endif
            % if inst_vars:
                <h3>Instance variables</h3>
                % for v in inst_vars:
                    <div class="item">
                    ${show_var(v)}
                    ${show_inheritance(v)}
                    ${show_member_desc(v)}
                    </div>
                % endfor
            % endif
            % if properties:
                <h3 title="Methods with @property">Computed properties</h3>
                % for p in properties:
                    ${show_var(p)}
                    ${show_inheritance(p)}
                    ${show_member_desc(p)}
                % endfor
            % endif
            % if methods:
                <h3>Methods</h3>
                % for f in methods:
                    ${show_class_func(f)}
                % endfor
            % endif
        </div>
    </div>
</%def>

<%def name="render_breadcrumbs(mod)">\
% for part, path, sep in breadcrumbs(mod.refname):
<a class="breadcrumblink" href="${path}">${part}</a>${sep}\
% endfor
</%def>

<%def name="show_module(module)">
    <%
    variables = module.variables()
    classes = module.classes()
    exceptions = module.exceptions()
    functions = module.functions()
    submodules = module.submodules()
    %>

    <header id="section-intro">
        <h1 class="modtitle">
            Module <span class="name">${render_breadcrumbs(module)}</span>
        </h1>
        ${show_desc(module)}
    </header>

    <section id="section-items">
        % if variables:
            <h2 class="sectiontitle" id="header-variables">Module variables</h2>
            % for v in variables:
                <div class="item">
                    ${show_var(v)}
                    ${show_desc(v)}
                </div>
            % endfor
        % endif

        % if functions:
            <h2 class="sectiontitle" id="header-functions">Functions</h2>
            % for f in functions:
                ${show_func(f)}
            % endfor
        % endif

        % if classes:
            <h2 class="sectiontitle" id="header-classes">Classes</h2>
            % for c in classes:
                ${show_class(c)}
            % endfor
        % endif

        % if exceptions:
            <h2 class="sectiontitle" id="header-exceptions">Exceptions</h2>
            % for c in exceptions:
                ${show_class(c)}
            % endfor
        %endif

        % if submodules:
            <h2 class="sectiontitle" id="header-submodules">Submodules</h2>
            % for m in submodules:
                <div class="item">
                    <a class="name" href="${obj_url(m)}">${m.name}</a>
                    ${desc(m, limit=300)}
                </div>
            % endfor
        % endif
    </section>
</%def>

<%def name="obj_list(objs)">
    <ul class="objlist">
    % for obj in objs:
        <li>${obj_link(obj)}</lI>
    % endfor
    </ul>
</%def>

<%def name="class_index(classes, title)">
    % if classes:
        <li class="indexsection">
            <h1><a href="#header-${title.lower()}" class="sectionlink">${title}</a></h1>
            <ul class="objlist">
            % for c in classes:
                <li>
                    ${obj_link(c)}
                    <%
                    methods = c.functions() + c.class_methods() + c.methods()
                    %>
                    % if methods:
                        ${obj_list(methods)}
                    % endif
                </li>
            % endfor
            </ul>
        </li>
    % endif
</%def>

<%def name="module_index(module)">
    <%
    variables = module.variables()
    classes = module.classes()
    exceptions = module.exceptions()
    functions = module.functions()
    submodules = module.submodules()

    show_index = variables or classes or exceptions or functions or submodules
    %>
    % if show_index:
        <div id="index-column">
            <ul id="index">
            % if variables:
                <li class="indexsection">
                    <h1><a href="#header-variables" class="sectionlink">Module variables</a></h1>
                    ${obj_list(variables)}
                </li>
            % endif

            % if functions:
                <li class="indexsection">
                    <h1><a href="#header-functions" class="sectionlink">Functions</a></h1>
                    ${obj_list(functions)}
                </li>
            % endif

            ${class_index(classes, "Classes")}
            ${class_index(exceptions, "Exceptions")}

            % if submodules:
                <li class="indexsection">
                    <h1><a href="#header-submodules" class="sectionlink">Submodules</a></h1>
                    ${obj_list(submodules)}
                </li>
            % endif
            </ul>
        </div>
    % endif
</%def>

<!doctype html>
<html>
<head>
    <!-- Documentation generated by pdoc3k -->

    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />

    <title>${module.name} API documentation</title>
    <meta name="description" content="${module.docstring | glimpse, trim}" />

    <style type="text/css">
        <%include file="normalize.css" />
    </style>

    % if use_pygments:
    <style type="text/css">
    ${HtmlFormatter(style="trac").get_style_defs(".codehilite")}
    </style>
    % endif

    <style type="text/css">
        <%include file="main.css" />
    </style>

    <style type="text/css">
        <%include file="print.css" />
    </style>
</head>
<body>
    <main>
        ${module_index(module)}
        <div id="content-column">
            <div id="content">
                ${show_module(module)}
            </div>
        </div>
    </main>

    <script defer>
        <%include file="toggle.js" />
    </script>

    % if use_latex:
    <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
        tex2jax: {
            inlineMath: [["$", "$"], ["\\(", "\\)"]]
        }
    });
    </script>

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
    % endif
</body>
</html>
