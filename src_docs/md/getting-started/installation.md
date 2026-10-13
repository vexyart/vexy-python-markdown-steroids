# Installation

## Requirements

- Python 3.12 or later.

Installing the package also installs everything the extensions import:

| Package | Minimum version | Used by |
|---|---|---|
| `markdown` | 3.5 | All extensions |
| `pymdown-extensions` | 10.2 | `keys` (escape handling), `wikilink` (slugs) |
| `mako` | 1.3 | `md_mako` |
| `PyYAML` | 6.0 | `meta_yaml` |
| `lxml` | 5.0 | `kill_tags`, `translate_no` |
| `cssselect` | 1.2 | `kill_tags`, `translate_no` (CSS selectors) |
| `beautifulsoup4` | 4.12 | `kill_tags`, `translate_no` (`normalize` option) |
| `html5lib` | 1.1 | `kill_tags`, `translate_no` (`normalize` option) |
| `filetype` | 1.2 | `img_smart` |
| `imageio` | 2.0 | `img_smart` |
| `requests` | 2.0 | `img_smart` (remote images) |
| `json-flatten` | 0.3 | Listed as a dependency; not imported by any extension |

## Install from PyPI

```bash
pip install vexy-python-markdown-steroids
```

With `uv`:

```bash
uv pip install vexy-python-markdown-steroids
```

For an MkDocs site, install the package into the same environment as MkDocs.
To try it in a one-off build without installing:

```bash
uvx --with vexy-python-markdown-steroids mkdocs build
```

## Install from source

1. Clone the repository:

    ```bash
    git clone https://github.com/vexyart/vexy-python-markdown-steroids.git
    cd vexy-python-markdown-steroids
    ```

2. Install it with the development tools:

    ```bash
    uv sync --extra dev
    ```

The version comes from the latest `vX.Y.Z` git tag through `hatch-vcs`.

## Check the installation

The import name is `mdx_steroids`, not the PyPI name:

```bash
python -c "import mdx_steroids; print(mdx_steroids.__version__)"
```

To check that an extension loads, convert a short string with it:

```bash
python -c "import markdown; print(markdown.markdown('Press ++ctrl+s++.', extensions=['mdx_steroids.keys']))"
```

The command prints:

```html
<p>Press <span class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd class="key-s">S</kbd></span>.</p>
```

!!! note "Video sizes in `img_smart`"
    `img_smart` reads video dimensions with the `pyav` plugin of `imageio`.
    That plugin needs the `av` package, which is not installed automatically.
    Without it, videos get no width. Install it with `pip install av` if you
    need video sizes.
