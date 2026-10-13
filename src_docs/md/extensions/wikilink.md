# wikilink

`mdx_steroids.wikilink` turns wiki-style links, `[[Page Name]]`, into Markdown
links. The page name becomes the link text, and a URL is built from the page
name.

## Example

With the default options, this Markdown:

```markdown
This is a [[Wiki Link]] and [[Ünïcode Page]].
```

becomes:

```html
<p>This is a <a href="/Wiki-Link/">Wiki Link</a> and <a href="/%C3%9Cn%C3%AFcode-Page/">Ünïcode Page</a>.</p>
```

With `base_url: /kb/`, `end_url: .html` and `space_sep: _`:

```markdown
This is a [[Wiki Link]].
```

```html
<p>This is a <a href="/kb/Wiki_Link.html">Wiki Link</a>.</p>
```

## How it works

The extension is a preprocessor: it rewrites the Markdown source before
Python-Markdown parses it.

1. On every line it finds `[[…]]` where the text inside contains no brackets
   and no line break.
2. It builds a slug from the text with the `slugify` function of
   `pymdownx.slugs`, with case kept as it is (`case="none"`) and percent
   encoding on. Spaces become `space_sep`; punctuation such as `&`, `:` and `!`
   is dropped; letters outside ASCII are percent-encoded.
3. It replaces `[[Text]]` with the Markdown link
   `[Text](base_url + slug + end_url)`.

Python-Markdown then turns that link into an `<a>` element.

Some results of step 2, with the default options:

| Markdown | `href` |
|---|---|
| `[[a]]` | `/a/` |
| `[[b c]]` | `/b-c/` |
| `[[C++ & Python: tips!]]` | `/C--Python-tips/` |
| `[[Ünïcode Page]]` | `/%C3%9Cn%C3%AFcode-Page/` |

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `base_url` | str | `"/"` | Text put before the slug. |
| `end_url` | str | `"/"` | Text put after the slug. |
| `space_sep` | str | `"-"` | Text that replaces spaces in the slug. |
| `html_class` | str | `"wikilink"` | Accepted but not used. The links have no class, because Python-Markdown builds them from ordinary Markdown links. |

## Limits

- **No custom link text.** `[[Page Name|Label]]` is not split at `|`. It
  becomes a link with the text `Page Name|Label` to `/Page-NameLabel/`. Write an
  ordinary Markdown link instead: `[Label](/Page-Name/)`.
- **Case is kept.** `[[Getting Started]]` links to `/Getting-Started/`. MkDocs
  builds URLs from file names, which are often lower case, such as
  `getting-started/`. Name the target file to match, or use ordinary links.
- **Code is not protected.** The extension works on raw lines, so `` `[[code]]` ``
  in inline code becomes `` `[code](/code/)` ``.
- In MkDocs, links that start with `/` are reported as absolute links and are
  not checked.

## Configuration examples

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.wikilink:
      base_url: /wiki/
      end_url: /
      space_sep: "-"
```

Python:

```python
import markdown

html = markdown.markdown(
    "See [[Wiki Link]].",
    extensions=["mdx_steroids.wikilink"],
    extension_configs={"mdx_steroids.wikilink": {"base_url": "/kb/", "end_url": ".html"}},
)
# <p>See <a href="/kb/Wiki-Link.html">Wiki Link</a>.</p>
```
