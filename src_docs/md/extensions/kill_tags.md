# kill_tags

`mdx_steroids.kill_tags` deletes HTML elements from the finished output. You
choose the elements with CSS selectors or XPath expressions. It also deletes
elements that are empty, such as a `<p>` with nothing in it.

## Example

With `kill: [".ad"]` and `kill_known: true`, this Markdown:

```markdown
Keep this <del>but not this</del>.

<p></p>

<div class="ad">Advert</div>

End.
```

becomes (blank lines shortened):

```html
<p>Keep this .</p>

<p>End.</p>
```

- `<del>but not this</del>` was removed by the built-in selectors that
  `kill_known: true` adds. The text after it, `.`, was kept.
- `<div class="ad">` matched the selector `.ad` and was removed with its
  content.
- The empty `<p></p>` was removed because `p` is in the default `kill_empty`
  list.

## How it works

The extension is a postprocessor: it runs on the HTML string after
Python-Markdown has serialised the document.

1. If `normalize` is true, it reparses the HTML with BeautifulSoup and
   `html5lib`.
2. It parses the HTML as a fragment with `lxml`, inside a temporary `<div>`.
3. It converts each entry of `kill` to XPath. An entry that starts with `!` is
   used as XPath directly; any other entry is a CSS selector and is converted
   with `cssselect`.
4. With `kill_known: true`, it adds two built-in XPath expressions (see below).
5. It removes every element that matches, with its content. Text that followed
   the element (its "tail") is kept and attached to the previous element or to
   the parent.
6. For each tag name in `kill_empty`, it removes elements of that name that
   contain no text (other than whitespace) and have no attributes, at any depth.
7. It serialises the fragment back to HTML. If `normalize` is true, it runs
   BeautifulSoup over the result again.

### The known selectors

`kill_known: true` adds these two XPath expressions:

```text
//pre[@class and contains(concat(' ', normalize-space(@class), ' '), ' highlight ') and code[@class and contains(concat(' ', normalize-space(@class), ' '), ' language-del ')]]
descendant-or-self::del
```

The first removes a highlighted code block whose language is `del`. The second
removes every `<del>` element. Together they let you keep text in the Markdown
source, visible in a plain preview such as GitHub, that never reaches the
built HTML:

````markdown
Visible paragraph.

```del
This block is visible on GitHub but removed from the HTML.
```

Visible ~~on GitHub only~~ text.
````

The first expression only matches `<pre class="highlight"><code class="language-del">`.
`pymdownx.superfences` produces that markup when `pymdownx.highlight` has
`use_pygments: false`. With Pygments turned on (the default), the class
`highlight` sits on a surrounding `<div>` and the block is not removed. The
`~~text~~` form needs `pymdownx.tilde`, which turns it into `<del>`.

This configuration removes both parts of the example above:

```yaml
markdown_extensions:
  - pymdownx.highlight:
      use_pygments: false
  - pymdownx.superfences
  - pymdownx.tilde
  - mdx_steroids.kill_tags:
      kill_known: true
```

The output is:

```html
<p>Visible paragraph.</p>

<p>Visible  text.</p>
```

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `kill` | list of str | `[]` | CSS selectors, or XPath expressions prefixed with `!`. Matching elements are removed with their content. |
| `kill_known` | bool | `false` | Also remove `<del>` elements and code blocks in the `del` language. |
| `kill_empty` | list of str | `["p", "div", "h1", "h2", "h3", "h4", "h5", "h6", "pre"]` | Tag names. Elements with these names are removed when they have no text and no attributes. |
| `normalize` | bool | `false` | Pass the HTML through BeautifulSoup (`html5lib`) before and after the removal. |

!!! warning "`normalize` adds a document wrapper"
    `html5lib` builds a full document, so with `normalize: true` the output is
    wrapped in `<html><head></head><body>…</body></html>`. Leave it off when the
    output is inserted into a page, as in MkDocs.

!!! note "Empty elements with attributes are kept"
    An empty element that has any attribute, such as `<div class="spacer"></div>`
    or `<p id="x"></p>`, is not removed by `kill_empty`. An element that only
    contains an image with a `src` is kept for the same reason.

## Configuration examples

MkDocs:

```yaml
markdown_extensions:
  - pymdownx.tilde
  - mdx_steroids.kill_tags:
      kill:
        - .advertisement-banner
        - "!//figure[not(img)]"
      kill_known: true
      kill_empty: [p, div, span]
```

Python, with an XPath selector:

```python
import markdown

html = markdown.markdown(
    '<div id="x">X</div>\n\nKeep.',
    extensions=["mdx_steroids.kill_tags"],
    extension_configs={"mdx_steroids.kill_tags": {"kill": ["!//div[@id='x']"]}},
)
# <p>Keep.</p>
```
