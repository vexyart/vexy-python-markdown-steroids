# replimgsrc

`mdx_steroids.replimgsrc` does a find-and-replace on the `src` of every image.
Use it to point images that were written for one location, such as a GitHub
repository, to another.

## Example

With `find: https://github.com/repo/blob/master/images/` and
`replace: ../img/`, this Markdown:

```markdown
![Logo](https://github.com/repo/blob/master/images/logo.png)
```

becomes:

```html
<p><img alt="Logo" src="../img/logo.png" /></p>
```

## How it works

After Python-Markdown has built the document tree, the extension visits every
`<img>` element:

- If `find` is not empty, it replaces every occurrence of `find` in `src` with
  `replace`.
- If `find` is empty, it puts `replace` in front of `src`.

With `find` empty and `replace: /static/`, `![Logo](logo.png)` becomes
`<img alt="Logo" src="/static/logo.png" />`. With both options empty, nothing
changes.

The replacement is plain text, not a pattern, and it applies to absolute and
relative paths alike. Images written as raw HTML are not in the document tree
and are not changed.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `find` | str | `""` | The text to look for in each image `src`. |
| `replace` | str | `""` | The replacement text, or a prefix when `find` is empty. |

## Configuration examples

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.replimgsrc:
      find: https://github.com/repo/blob/master/images/
      replace: ../img/
```

Python:

```python
import markdown

html = markdown.markdown(
    "![Logo](logo.png)",
    extensions=["mdx_steroids.replimgsrc"],
    extension_configs={"mdx_steroids.replimgsrc": {"replace": "/static/"}},
)
# <p><img alt="Logo" src="/static/logo.png" /></p>
```

## replimgsrc or absimgsrc

| | `replimgsrc` | `absimgsrc` |
|---|---|---|
| Changes | Every image | Only relative images |
| Method | Text replacement, or a prefix | URL join with `urljoin()` |
| Typical use | Move images from one known location to another | Serve all local images from a CDN |

Both run as tree processors with priority 0, so the one you load first runs
first. With `absimgsrc` (`base_url: https://cdn/`) loaded before `replimgsrc`
(`replace: /s/`), `![a](x.png)` becomes `src="/s/https://cdn/x.png"`. In the
opposite order it becomes `src="https://cdn/s/x.png"`.
