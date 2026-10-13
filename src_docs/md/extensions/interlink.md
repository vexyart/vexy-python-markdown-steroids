# interlink

`mdx_steroids.interlink` lets you write short internal links, such as
`[Setup](setup)`, and turns them into full URLs by adding a prefix and a suffix.
Links that contain a protocol or a period are left alone.

## Example

With `base_url: /docs/` and `end_url: /`, this Markdown:

```markdown
See [setup](setup#install), [home](index), [ext](https://ex.com), [file](a.html).
```

becomes:

```html
<p>See <a href="/docs/setup/#install">setup</a>, <a href="/docs/index/">home</a>, <a href="https://ex.com">ext</a>, <a href="a.html">file</a>.</p>
```

- `setup#install` became `/docs/setup/#install`: the suffix goes before the
  anchor.
- `https://ex.com` contains `://` and was not changed.
- `a.html` contains a period and was not changed.

## How it works

The extension is a preprocessor: it rewrites the Markdown source before
Python-Markdown parses it. On every line, it looks for inline links of the form
`[text](target)`, where `target` contains no spaces. Image links (`![…](…)`)
are skipped.

For each link:

1. If the target contains `://` or `.`, the link is left as it is.
2. The target is split at `#`. If the part before `#` is empty (a link to an
   anchor on the same page, such as `#intro`), the link is left as it is.
3. Otherwise the new target is `base_url` + page + `end_url`, followed by `#`
   and the anchor if there was one.

The rewritten link is ordinary Markdown, so Python-Markdown then turns it into
an `<a>` element as usual.

Because the extension works on raw lines, it also rewrites links inside code
blocks and inline code. Links with a title (`[text](target "title")`) contain a
space and are not matched.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `base_url` | str | `""` | Text put before the page name. |
| `end_url` | str | `""` | Text put after the page name, before any `#anchor`. |

With both options empty, the extension changes nothing.

## Configuration examples

Python:

```python
import markdown

html = markdown.markdown(
    "See [setup](setup#install).",
    extensions=["mdx_steroids.interlink"],
    extension_configs={"mdx_steroids.interlink": {"base_url": "/docs/", "end_url": "/"}},
)
# <p>See <a href="/docs/setup/#install">setup</a>.</p>
```

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.interlink:
      base_url: /docs/
      end_url: /
```

## interlink or wikilink

| | `interlink` | `wikilink` |
|---|---|---|
| Syntax | `[text](page)` | `[[Page Name]]` |
| Link text | Your own | The page name |
| Changes the page name | No | Yes: turns spaces into `space_sep` and percent-encodes |
| Defaults | No prefix or suffix | `/` prefix and suffix |
