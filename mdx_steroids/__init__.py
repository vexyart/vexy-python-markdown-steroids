# this_file: mdx_steroids/__init__.py
"""mdx_steroids: small collection of Python Markdown extensions."""

try:
    from mdx_steroids.__version__ import __version__
except ImportError:  # editable install before hatch-vcs has run
    __version__ = "0.0.0+local"

__all__ = [
    "absimgsrc",
    "figcapkbd",
    "keymap_db",
    "keys",
    "kill_tags",
    "md_mako",
    "meta_yaml",
    "replimgsrc",
    "util",
    "wikilink",
    "comments",
    "interlink",
    "img_smart",
    "__version__",
]
