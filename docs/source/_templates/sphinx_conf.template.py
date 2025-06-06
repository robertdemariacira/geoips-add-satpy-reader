# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""GeoIPS PKGNAME documentation build configuration file."""

import sys
import os
import geoips

VERSION = str(geoips.__version__)

source_path = os.path.dirname(os.path.abspath(__file__))

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.append(os.path.abspath('.'))
sys.path.insert(0, os.path.abspath("../sphinxext"))
sys.path.extend(
    [
        # numpy standard doc extensions
        os.path.join(os.path.dirname(__file__), "..", "../..", "sphinxext")
    ]
)

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = "5.3.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxarg.ext",
    "sphinxcontrib.autoprogram",
    "m2r2",
    "sphinxcontrib.mermaid",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = [".rst"]

# The encoding of source files.
source_encoding = "utf-8"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "GeoIPS, Geolocated Information Processing System"
copyright = "NOT APPLICAPABLE"
author = "the U.S. NAVAL RESEARCH LABORATORY"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents. Consider setting version=release=VERSION
#
# The full version, including alpha/beta/rc tags.
release = "{0}".format(VERSION)
# The short X.Y version.
version = "{0}".format(VERSION[0:3])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

exclude_patterns = [
    "**.ipynb_checkpoints",
    # to ensure that include files (partial pages) aren't built, exclude them
    # https://github.com/sphinx-doc/sphinx/issues/1965#issuecomment-124732907
    "**/includes/**",
    "import/*",
]

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "pydata_sphinx_theme"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "external_links": [],
    "navigation_with_keys": False,
    "footer_end": ["geoips_footer"],
    "github_url": "https://github.com/NRLMMD-GEOIPS/PKGNAME",
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "logo": {
        "image_light": "_static/NRL_logo_RGB.jpg",
        "image_dark": "_static/NRL_logo_sidebar_Reverse.png",
    },
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/NRL_logo_sidebar_Reverse.png"

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or
# 32x32 pixels large.
html_favicon = "_static/nrlicon.ico"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y %H:%M:%S"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# US Navy does not copyright
html_show_copyright = False

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
html_search_language = "en"

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = "GeoIPS_PKGNAME_doc"

# -- Options for LaTeX output ---------------------------------------------

# Latex additional files to include to format header footer for PDF.
latex_additional_files = ["fancyhf.sty"]

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    "preamble": r"\usepackage{fancyhf}\usepackage{enumitem}\setlistdepth{99}",
    # Latex figure (float) alignment
    "figure_align": "H",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
pkgnamelatex = "PKGNAME".split("_")
if len(pkgnamelatex) > 1:
    # set up latex escape
    pkgnamelatex = r"\_".join(pkgnamelatex)
latex_documents = [
    (
        master_doc,
        "GeoIPS_PKGNAME.tex",
        "GeoIPS {0} Documentation".format(pkgnamelatex),
        "U.S. NAVAL RESEARCH LABORATORY",
        "manual",
        False,
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_static/NRL_logo_RGB.jpg"

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, "GeoIPS_PKGNAME", "GeoIPS PKGNAME Documentation", [author], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "GeoIPS_PKGNAME",
        "GeoIPS PKGNAME Documentation",
        author,
        "NRL-MMD",
        "Geolocated Information Processing System.",
        "packages: interface, modules, tools",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False


# setup and rstjinja based on pandas-doc rendering
def rstjinja(app, docname, source):
    """Render our pages as a jinja template for fancy templating goodness."""
    # https://www.ericholscher.com/blog/2016/jul/25/integrating-jinja-rst-sphinx/
    # Make sure we're outputting HTML
    if app.builder.format != "html":
        return
    src = source[0]
    rendered = app.builder.templates.render_string(src, app.config.html_context)
    source[0] = rendered


# need min:max width limits ref https://stackoverflow.com/a/43186995/1480918
def setup(app):
    """Css width setup."""
    app.add_css_file("set_width.css")
    """Jinja setup function."""
    app.connect("source-read", rstjinja)
