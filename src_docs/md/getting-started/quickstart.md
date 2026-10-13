# Quick start

This page uses two extensions, `wikilink` and `keys`, in three ways: from
Python, from the `python -m markdown` command and from MkDocs. The input is the
same each time:

```markdown
# Notes

See [[Getting Started]] and press ++ctrl+s++ to save.
```

## Prerequisites

- The package is installed (see [Installation](installation.md)).

## From Python

1. Pass the extension names to `markdown.markdown()`:

    ```python
    import markdown

    text = "# Notes\n\nSee [[Getting Started]] and press ++ctrl+s++ to save."
    html = markdown.markdown(
        text,
        extensions=["mdx_steroids.wikilink", "mdx_steroids.keys"],
    )
    print(html)
    ```

2. Run the script. It prints:

    ```html
    <h1>Notes</h1>
    <p>See <a href="/Getting-Started/">Getting Started</a> and press <span class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd class="key-s">S</kbd></span> to save.</p>
    ```

What happened:

- `wikilink` replaced `[[Getting Started]]` with the Markdown link
  `[Getting Started](/Getting-Started/)` before parsing. The default
  `base_url` and `end_url` are both `/`, and spaces become `-`.
- `keys` turned `++ctrl+s++` into a `<span class="keys">` with one `<kbd>` per
  key and a `<span>+</span>` between them.

To change options, pass `extension_configs`:

```python
html = markdown.markdown(
    text,
    extensions=["mdx_steroids.wikilink", "mdx_steroids.keys"],
    extension_configs={
        "mdx_steroids.wikilink": {"base_url": "/wiki/", "end_url": ".html"},
        "mdx_steroids.keys": {"strict": True},
    },
)
```

The link now points to `/wiki/Getting-Started.html`, and the keys are wrapped in
an outer `<kbd class="keys">` instead of a `<span>`.

## From the command line

Python-Markdown has a command-line interface. It reads extension options from a
JSON or YAML file.

1. Save the Markdown as `input.md`.
2. Save the options as `config.yml`:

    ```yaml
    mdx_steroids.wikilink:
      base_url: /wiki/
      end_url: .html
    mdx_steroids.keys:
      strict: true
    ```

3. Run:

    ```bash
    python -m markdown -x mdx_steroids.wikilink -x mdx_steroids.keys -c config.yml input.md -f output.html
    ```

`output.html` contains:

```html
<h1>Notes</h1>
<p>See <a href="/wiki/Getting-Started.html">Getting Started</a> and press <kbd class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd class="key-s">S</kbd></kbd> to save.</p>
```

Every extension named in `config.yml` must also be loaded with `-x`.

## From MkDocs

1. Install the package into the environment that runs MkDocs.
2. Add the extensions to `markdown_extensions` in `mkdocs.yml`:

    ```yaml
    markdown_extensions:
      - mdx_steroids.wikilink:
          base_url: /
          end_url: /
      - mdx_steroids.keys
    ```

3. Run `mkdocs build`.

MkDocs passes each page through the extensions. In the built page, the text
reads "See Getting Started and press Ctrl+S to save", with a link and styled
keys.

!!! note
    MkDocs reports a link that starts with `/` as an absolute link and leaves it
    unchanged. `wikilink` keeps the capital letters of the page name, so
    `[[Getting Started]]` links to `/Getting-Started/`. Make sure the target
    page has that URL; see [wikilink](../extensions/wikilink.md).

## Next steps

- [Configuration](configuration.md) lists the ways to pass options and the
  option types.
- The [extension pages](../extensions/index.md) describe each extension.
