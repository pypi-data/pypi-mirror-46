# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set
# to its containing dir.

import nengo_sphinx_theme

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.githubpages",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "nengo_sphinx_theme",
]


# -- sphinx
nitpicky = True
nitpick_ignore = [
    ('py:class', 'int'),
    ('py:class', 'bool'),
    ('py:class', 'str'),
    ('py:exc', 'TypeError'),
]
exclude_patterns = ["_build", "**/.ipynb_checkpoints"]
source_suffix = ".rst"
source_encoding = "utf-8"
master_doc = "index"
project = u"Nengo Sphinx theme"
authors = u"Applied Brain Research"
copyright = nengo_sphinx_theme.__copyright__
version = ".".join(nengo_sphinx_theme.__version__.split(".")[:2])
release = nengo_sphinx_theme.__version__

# -- sphinx.ext.todo
todo_include_todos = True

# -- Options for HTML output --------------------------------------------------

pygments_style = "sphinx"
templates_path = []

html_title = "Nengo Sphinx theme v{}".format(release)
html_theme = "nengo_sphinx_theme"
html_last_updated_fmt = ""  # Suppress "Last updated on:" timestamp
html_context = {
    "building_version": "latest",
    "releases": "404",
}
html_theme_options = {
    "sidebar_logo_width": 100,
    "sidebar_toc_depth": 4,
    "nengo_logo": "general-full-light.svg",
    "analytics_id": "UA-41658423-2",
}

# -- Options for LaTeX output -------------------------------------------------

latex_documents = [
    # (source start file, target, title, author, documentclass [howto/manual])
    ("index", "nengo-sphinx-theme.tex", html_title, authors, "manual"),
]

# -- Options for manual page output -------------------------------------------

man_pages = [
    # (source start file, name, description, authors, manual section).
    ("index", "nengo-sphinx-theme", html_title, [authors], 1)
]
