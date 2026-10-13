# comments

`mdx_steroids.comments` removes comments that start with three dashes,
`<!---`, from the output. Ordinary HTML comments, `<!--`, stay in the HTML. Use
the three-dash form for notes to yourself and other writers.

The extension has no options.

## Example

This Markdown:

```markdown
Visible.

<!--- removed -->

<!-- kept -->

Text <!--- inline gone --> end.

<!---
multi
line
-->
After.
```

becomes:

```html
<p>Visible.</p>
<!-- kept -->

<p>Text end.</p>
<p>After.</p>
```

- The block comment `<!--- removed -->` is gone.
- The ordinary comment `<!-- kept -->` is still in the HTML.
- The inline comment and the whitespace before it are gone; `Text end.` remains.
- The comment that spans three lines is gone, and the text after `-->` stays.

## How it works

The extension works on the source text, in three steps:

1. **Protect.** A preprocessor replaces every `<!---` with a placeholder string,
   so that Python-Markdown does not treat it as an HTML comment.
2. **Remove.** A second preprocessor removes everything from a placeholder up to
   the next `-->`, together with the whitespace before the placeholder. If there
   is no `-->` on the same line, it removes the rest of the line and every
   following line up to the line that contains `-->`. Text after that `-->` is
   kept.
3. **Restore.** A postprocessor turns any placeholder that is left in the HTML
   back into `<!---`.

### Comments inside code

Step 2 runs on the raw source, so it can also reach code. With
`extensions=["mdx_steroids.comments", "fenced_code"]`:

| Source | Result |
|---|---|
| A fenced code block (```` ``` ````) that contains `<!--- x -->` | Kept. `fenced_code` stores the block before step 2 runs, and step 3 restores `<!---`. |
| An indented code block that contains `<!--- x -->` | The comment is removed from the code. |
| Inline code such as `` `<!---` `` with no `-->` on the line | Starts a multi-line comment. Everything up to the next `-->`, even in later paragraphs, is removed. |

To show the three-dash marker in running text, put it in a fenced code block or
write it as `&lt;!---`.

## Configuration examples

Python:

```python
import markdown

html = markdown.markdown(text, extensions=["mdx_steroids.comments"])
```

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.comments
```
