# project information
author = "Akio Taniguchi"
copyright = "2023-2024 Akio Taniguchi"


# general configuration
add_module_names = False
autodoc_default_options = {
    "special-members": "__call__, __getitem__",
}
autodoc_member_order = "bysource"
autodoc_typehints = "both"
autodoc_typehints_format = "short"
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]
myst_heading_anchors = 3
templates_path = ["_templates"]


# options for HTML output
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "github_url": "https://github.com/astropenguin/dataspecs/",
    "logo": {"text": "dataspecs"},
}
