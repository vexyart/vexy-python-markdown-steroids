# md_mako

`mdx_steroids.md_mako` runs the Markdown source through the
[Mako](https://www.makotemplates.org/) template engine before Python-Markdown
parses it. You can use variables, Python expressions, loops, conditions and
included files in your Markdown.

## Example

Configuration:

```yaml
markdown_extensions:
  - mdx_steroids.meta_yaml
  - mdx_steroids.md_mako:
      meta:
        product: FontLab
        author: Nobody
```

Markdown:

```markdown
---
author: John Doe
---
## Heading

${author} wrote this for ${product}.

% for n in ['one', 'two']:
* ${n}
% endfor
```

HTML:

```html
<h2>Heading</h2>
<p>John Doe wrote this for FontLab.</p>
<ul>
<li>one</li>
<li>two</li>
</ul>
```

- `meta_yaml` removed the front matter and stored `author: John Doe`.
- `md_mako` rendered the page with the variables from `meta` (`product`,
  `author`), then replaced `author` with the value from the front matter.
- The `% for` loop produced one list item per value.
- The `## Heading` line stayed a heading, although `##` starts a comment in Mako.

## Mako syntax in Markdown

| Syntax | Meaning |
|---|---|
| `${expression}` | Insert the value of a Python expression |
| `% for …:` … `% endfor` | Loop; the `%` must be the first character on the line |
| `% if …:` … `% else:` … `% endif` | Condition |
| `<%include file="name.md"/>` | Insert another file, also rendered by Mako |
| `<%! … %>` | Module-level Python code, for example imports and functions |
| `<% … %>` | Python code that runs while the page is rendered |
| `%%` at the start of a line | A literal `%` |
| `${"$"}{…}` | A literal `${…}` |

A `%` or `$` in the middle of a line, as in `50% of users` or `$5`, is kept as
it is.

See the [Mako documentation](https://docs.makotemplates.org/en/latest/syntax.html)
for the full syntax.

## How it works

1. If `python_block` names a file that exists, its content is put at the start
   of the source inside `<%! … %>`, so its functions and imports are available
   in the page.
2. If `include_auto` is set, `<%include file="…"/>` for that file is put at the
   very start.
3. Lines that start with `#`, `{%` or `%}` are protected so that Mako leaves
   them alone. This keeps Markdown headings, which Mako would read as comments
   (`##`), and template tags meant for other tools.
4. The variables are collected: first everything from `meta`, then everything
   from `md.Meta`, if another extension such as `meta_yaml` has filled it.
   Front-matter keys are lower-cased, and list values are joined into one
   string. Front matter wins over `meta`.
5. Mako renders the source with `strict_undefined=True`. The result replaces
   the source, and Python-Markdown continues with it.

The same heading protection applies to files loaded with `<%include>`.

### Order with `meta_yaml`

`meta_yaml` runs before `md_mako` (priority 29 against 28), so the front matter
is already parsed and removed when Mako runs. Without `meta_yaml`, the front
matter is ordinary text: Mako passes it through, and Python-Markdown renders
the `---` lines as rules and the `key: value` line as text.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `meta` | dict | `{}` | Variables available in every page. Front matter overrides them. |
| `include_base` | str or list | `"."` | Folder, or list of folders, where `<%include file="…"/>` looks for files. Relative folders are resolved against the current working directory. |
| `include_encoding` | str | `"utf-8"` | Encoding of the page source passed to Mako. |
| `include_auto` | str | `""` | A file included at the start of every page. An absolute path is split into folder and file name, and the folder is searched first. |
| `python_block` | str | `""` | A Python file whose content is added at the start of every page as a `<%! … %>` block. |

### `python_block` lookup

The extension looks for the `python_block` file in two places:

1. The path as given, relative to the current working directory.
2. `include_base[0]` joined with the path.

The second rule only works when `include_base` is a list. If `include_base` is a
string, `include_base[0]` is its first character, so a string such as
`"includes"` makes the extension look in a folder named `i`. Give
`include_base` as a list, or give `python_block` as a path from the working
directory:

```yaml
markdown_extensions:
  - mdx_steroids.md_mako:
      include_base: [includes]
      python_block: helpers.py      # found as includes/helpers.py
```

If the file is not found in either place, the option is ignored without a
message.

## Example with includes and helpers

Folder layout:

```text
includes/
├── head.md        # *Draft for ${product}.*
├── notice.md      # Note: this page is about ${product}.
└── helpers.py
```

`includes/helpers.py`:

```python
import datetime

def year():
    return datetime.date(2026, 1, 1).year
```

Configuration:

```python
extension_configs = {
    "mdx_steroids.md_mako": {
        "include_base": ["includes"],
        "include_auto": "head.md",
        "python_block": "helpers.py",
        "meta": {"product": "FontLab"},
    }
}
```

Markdown, converted with `meta_yaml` and `md_mako`:

```markdown
---
author: John Doe
---
## Heading

${author}, ${year()}.

<%include file="notice.md"/>
```

HTML:

```html
<p><em>Draft for FontLab.</em></p>
<h2>Heading</h2>
<p>John Doe, 2026.</p>
<p>Note: this page is about FontLab.</p>
```

## Use front matter as variables

Load `meta_yaml` before `md_mako`. Every front-matter key becomes a variable
with a lower-case name:

```markdown
---
Title: Release notes
Version: 8.4
---
# ${title} for version ${version}
```

`meta_yaml` reads every value as a string, so `${version}` prints `8.4`.

## Errors

The extension does not catch Mako errors. They stop the conversion:

- An undefined variable raises `NameError`, for example
  `NameError: 'missing' is not defined`, because `strict_undefined` is on.
- A Mako syntax error, such as a `% for` without `% endfor`, raises a Mako
  exception.

In MkDocs, either error stops the build.
