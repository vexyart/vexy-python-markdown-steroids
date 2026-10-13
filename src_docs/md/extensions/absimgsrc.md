# absimgsrc

`mdx_steroids.absimgsrc` prepends a base URL to every relative image path. Use
it when the images of a document are served from another host, such as a CDN,
or when the same HTML is shown at several URL depths.

## Example

With `base_url: https://cdn.example.com/docs`, this Markdown:

```markdown
![Alt text](images/photo.jpg)

![x](/abs/a.png)

![y](https://ex.com/b.png)
```

becomes:

```html
<p><img alt="Alt text" src="https://cdn.example.com/docs/images/photo.jpg" /></p>
<p><img alt="x" src="https://cdn.example.com/abs/a.png" /></p>
<p><img alt="y" src="https://ex.com/b.png" /></p>
```

## How it works

After Python-Markdown has built the document tree, the extension visits every
`<img>` element that has a `src` attribute.

1. It checks whether the `src` is relative. A `src` is absolute, and left
   alone, if it starts with `http` or `//`, or with one of these schemes:
   `ftp://`, `ftps://`, `mailto:`, `news:`, `telnet://`, `file://`, `data:`,
   `tel:`, `ssh://`, `sftp://`.
2. If `base_url` is empty, it leaves the `src` alone.
3. If `base_url` does not end with `/` and the path does not start with `/`, it
   adds a `/` to `base_url`.
4. It joins the two with Python's `urllib.parse.urljoin()` and writes the
   result back to `src`.

Because of step 4, a path that starts with `/` replaces the whole path of
`base_url`: `/abs/a.png` with base `https://cdn.example.com/docs` gives
`https://cdn.example.com/abs/a.png`, as in the example above.

The extension only changes images written in Markdown syntax. An `<img>` tag
written as raw HTML in the Markdown source, such as `<img src="raw.png">`, keeps
its `src`, because raw HTML is not part of the document tree.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `base_url` | str | `""` | The URL to put in front of relative image paths. Empty means "change nothing". |

## Configuration examples

Python:

```python
import markdown

html = markdown.markdown(
    "![Alt text](images/photo.jpg)",
    extensions=["mdx_steroids.absimgsrc"],
    extension_configs={"mdx_steroids.absimgsrc": {"base_url": "https://cdn.example.com/"}},
)
# <p><img alt="Alt text" src="https://cdn.example.com/images/photo.jpg" /></p>
```

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.absimgsrc:
      base_url: https://cdn.example.com/
```

!!! warning
    In MkDocs, absolute image URLs are not checked or copied by MkDocs. Make sure
    the images exist at the new location.
