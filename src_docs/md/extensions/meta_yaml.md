# meta_yaml

`mdx_steroids.meta_yaml` reads a YAML block at the top of a Markdown document,
removes it from the text and stores the values in the `Meta` attribute of the
`Markdown` object. It is by Bernhard Fisseni and based on the meta-data
extension of Python-Markdown.

The extension has no options.

## Example

```python
import markdown

md = markdown.Markdown(extensions=["mdx_steroids.meta_yaml"])
html = md.convert("---\nTitle: Test Doc\nTags: [a, b]\nCount: 3\n---\n\nThe body.")
print(html)
print(md.Meta)
```

Output:

```text
<p>The body.</p>
{'title': ['Test Doc'], 'tags': ['a', 'b'], 'count': ['3']}
```

- The YAML block is not in the HTML.
- Keys are lower-cased: `Title` became `title`.
- Every value is a list. A single value is wrapped in a list; a YAML list stays
  a list.
- Every scalar is a string. `3` became `'3'`.

## Syntax

The block must start on the first line of the document:

```markdown
---
title: My page
author: Alex Doe
tags: [python, markdown]
---

The content starts here.
```

- The first line is exactly `---`.
- The second line must look like a key: a word (letters, digits, `_`, `-`),
  optional spaces and a colon. Otherwise the `---` is treated as a horizontal
  rule and nothing is read. This lets a document start with a rule.
- The block ends at the first line that is exactly `---` or `...`.

## How it works

The extension is a preprocessor with priority 29, so it runs before most other
preprocessors, including [`md_mako`](md_mako.md) (28).

1. It sets `md.Meta` to an empty dict.
2. If the first line is `---` and the second line looks like `key:`, it
   collects lines up to the closing `---` or `...` and removes them from the
   document.
3. It parses the collected lines with PyYAML's `BaseLoader` (the C version,
   `CBaseLoader`, when available). `BaseLoader` does not convert types, so
   numbers, booleans and dates stay strings.
4. It lower-cases the top-level keys, wraps each value that is not a list in a
   list, and stores the result in `md.Meta`.

Nested mappings are kept as dicts inside the list:

```yaml
---
title: A
nested:
  key: value
flag: true
---
```

gives `{'title': ['A'], 'nested': [{'key': 'value'}], 'flag': ['true']}`.

The value format, lower-case keys and lists, matches Python-Markdown's own
`meta` extension, so tools written for that extension can read `md.Meta`.

## Reusing a `Markdown` object

`md.Meta` is reset at the start of each conversion. After
`md.convert("Two")` on a document without front matter, `md.Meta` is `{}`.

For an empty document, Python-Markdown returns early without running the
preprocessors. If the object has never converted a non-empty document,
`md.Meta` does not exist yet.

## Errors

The extension does not catch YAML errors:

- A block without a closing `---` or `...` takes the rest of the document as
  YAML, which usually fails with `yaml.scanner.ScannerError`.
- Invalid YAML, such as `title: [unclosed`, raises a `yaml` exception such as
  `ParserError`.

## Configuration examples

MkDocs reads front matter itself, before Markdown conversion, so you do not need
this extension for MkDocs page metadata. Use it when you call Python-Markdown
directly, or together with `md_mako`:

```yaml
markdown_extensions:
  - mdx_steroids.meta_yaml
  - mdx_steroids.md_mako
```
