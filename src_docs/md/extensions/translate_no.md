# translate_no

`mdx_steroids.translate_no` adds `translate="no"` and the class `notranslate` to
chosen HTML elements. Browser translation tools, such as the one built into
Chrome, leave elements marked this way untranslated. By default it marks code,
key names and highlighted text.

## Example

With the default options, and with `keys` and `pymdownx.mark` also loaded, this
Markdown:

```markdown
Use `print()` and ++ctrl+c++ ==here==.
```

becomes:

```html
<p>Use <code translate="no" class="notranslate">print()</code> and <span class="keys"><kbd class="key-control notranslate" translate="no">Ctrl</kbd><span>+</span><kbd class="key-c notranslate" translate="no">C</kbd></span> <mark translate="no" class="notranslate">here</mark>.</p>
```

The `<code>`, `<kbd>` and `<mark>` elements are marked. Existing classes, such
as `key-control`, are kept.

## How it works

The extension is a postprocessor: it runs on the finished HTML string.

1. If `normalize` is true, it reparses the HTML with BeautifulSoup and
   `html5lib`.
2. It parses the HTML with `lxml.html.fromstring()`.
3. It converts each entry of `add` to XPath. An entry that starts with `!` is
   used as XPath directly; any other entry is a CSS selector and is converted
   with `cssselect`.
4. For every element that matches, it sets `translate="no"` and adds the class
   `notranslate`.
5. It serialises the tree back to HTML. If `normalize` is true, it runs
   BeautifulSoup over the result again.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `add` | list of str | `["code", "mark", "pre", "kbd"]` | CSS selectors, or XPath expressions prefixed with `!`, of the elements to mark. |
| `normalize` | bool | `false` | Pass the HTML through BeautifulSoup (`html5lib`) before and after marking. With this option the output is wrapped in `<html><head></head><body>…</body></html>`. |

Setting `add` replaces the default list. To keep the defaults and add more,
list them all:

```yaml
markdown_extensions:
  - mdx_steroids.translate_no:
      add: [code, mark, pre, kbd, .product-name]
```

With `add: [strong]`, `Use the **Glyph** panel.` becomes:

```html
<p>Use the <strong translate="no" class="notranslate">Glyph</strong> panel.</p>
```

## Output with several top-level elements

`lxml.html.fromstring()` wraps a fragment with several top-level elements in a
`<div>`. A document of two paragraphs therefore comes back as
`<div><p>…</p><p>…</p></div>`. Take this into account if your CSS or later
processing expects the paragraphs at the top level.

## Configuration examples

Python:

```python
import markdown

html = markdown.markdown(
    "Use `print()`.",
    extensions=["mdx_steroids.translate_no"],
)
# <p>Use <code translate="no" class="notranslate">print()</code>.</p>
```

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.keys
  - mdx_steroids.translate_no
```
