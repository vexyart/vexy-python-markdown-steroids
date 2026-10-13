# Configuration

Every extension takes its options as keyword arguments. Python-Markdown passes
them in from `extension_configs`, from a `-c` file on the command line, or from
the `markdown_extensions` list in MkDocs. This page shows the three forms and
summarises the options of all extensions.

## Three ways to pass options

### Python

Use the dotted extension name as the key in `extension_configs`:

```python
import markdown

html = markdown.markdown(
    text,
    extensions=["mdx_steroids.absimgsrc", "mdx_steroids.kill_tags"],
    extension_configs={
        "mdx_steroids.absimgsrc": {"base_url": "https://cdn.example.com/"},
        "mdx_steroids.kill_tags": {"kill": [".draft"], "kill_known": True},
    },
)
```

You can also create the extension object yourself. Every module has a
`makeExtension()` function that accepts the options:

```python
from mdx_steroids.absimgsrc import makeExtension

html = markdown.markdown(text, extensions=[makeExtension(base_url="https://cdn.example.com/")])
```

### Command line

`python -m markdown -c FILE` reads a JSON or YAML file with the same structure as
`extension_configs`. Load each configured extension with `-x` as well:

```bash
python -m markdown -x mdx_steroids.absimgsrc -c config.yml input.md
```

### MkDocs

Give the options under the extension name in `markdown_extensions`:

```yaml
markdown_extensions:
  - mdx_steroids.absimgsrc:
      base_url: https://cdn.example.com/
  - mdx_steroids.kill_tags:
      kill:
        - .draft
      kill_known: true
```

An extension without options is listed by name alone:

```yaml
markdown_extensions:
  - mdx_steroids.comments
```

## All options

| Extension | Option | Type | Default |
|---|---|---|---|
| `absimgsrc` | `base_url` | str | `""` |
| `comments` | — | | |
| `figcap` | — | | |
| `img_smart` | `find` | str | `""` |
| | `repl_path` | str | `""` |
| | `repl_url` | str | `""` |
| | `alt_figure` | bool | `false` |
| | `cache` | str | `""` |
| | `lazy` | bool | `false` |
| `interlink` | `base_url` | str | `""` |
| | `end_url` | str | `""` |
| `keys`, `kbd` | `separator` | str | `"+"` |
| | `strict` | bool | `false` |
| | `class` | str | `"keys"` |
| | `camel_case` | bool | `false` |
| | `key_map` | dict | `{}` |
| `kill_tags` | `normalize` | bool | `false` |
| | `kill` | list of str | `[]` |
| | `kill_known` | bool | `false` |
| | `kill_empty` | list of str | `["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "pre"]` |
| `md_mako` | `include_base` | str or list | `"."` |
| | `include_encoding` | str | `"utf-8"` |
| | `include_auto` | str | `""` |
| | `python_block` | str | `""` |
| | `meta` | dict | `{}` |
| `meta_yaml` | — | | |
| `replimgsrc` | `find` | str | `""` |
| | `replace` | str | `""` |
| `translate_no` | `normalize` | bool | `false` |
| | `add` | list of str | `["code", "mark", "pre", "kbd"]` |
| `wikilink` | `base_url` | str | `"/"` |
| | `end_url` | str | `"/"` |
| | `space_sep` | str | `"-"` |
| | `html_class` | str | `"wikilink"` (not used) |

Each extension page explains its options in detail.

## Combining extensions

Some extensions are designed to work together:

- `meta_yaml` with `md_mako`: the YAML front matter becomes template variables.
  See [md_mako](../extensions/md_mako.md#use-front-matter-as-variables).
- `keys` with `translate_no`: `translate_no` marks the `<kbd>` elements that
  `keys` creates, so browser translation leaves key names alone.
- `kill_tags` with `pymdownx.tilde`: `~~text~~` becomes `<del>`, which
  `kill_known: true` removes.

Do not combine `absimgsrc`, `replimgsrc` and `img_smart` without checking the
result: all three change image `src` attributes. See
[Architecture](../development/architecture.md) for the order in which they run.
