# keys

`mdx_steroids.keys` renders keyboard input. Write keys between `++` and `++`,
joined with `+`, and the extension turns them into `<kbd>` elements with a CSS
class per key. It is a fork of `pymdownx.keys` by Isaac Muse with its own key
list (see [Key name reference](keys-reference.md)).

## Example

With `camel_case: true`, this Markdown:

```markdown
Press ++Shift+Alt+PgUp++, type in ++"Hello"++ and press ++Enter++.
```

becomes:

```html
<p>Press <span class="keys"><kbd class="key-shift">Shift</kbd><span>+</span><kbd class="key-alt">Alt</kbd><span>+</span><kbd class="key-page-up">PgUp</kbd></span>, type in <span class="keys"><kbd>Hello</kbd></span> and press <span class="keys"><kbd class="key-enter">Enter</kbd></span>.</p>
```

- Each key became a `<kbd>` with the class `key-<name>` and the displayed text
  from the key list.
- `PgUp` is an alias of `page-up`, so its class is `key-page-up`.
- `"Hello"` is a quoted string, so it became a `<kbd>` with the text as written
  and no `key-` class.
- The whole group is wrapped in `<span class="keys">`, and `<span>+</span>`
  separates the keys.

## Syntax

| Markdown | Meaning |
|---|---|
| `++enter++` | One key |
| `++ctrl+alt+del++` | A combination; keys are joined with `+` |
| `++"Hello world"++` or `++'Hello'++` | Text to type, shown as written |
| `++ctrl+"c"++` | Keys and quoted text can be mixed |
| `\++ctrl++` | A backslash before `++` keeps the text literal: `++ctrl++` |

Key names may contain letters, digits, `_` and `-`. Inside quotes, a backslash
escapes the next character.

## How a key is looked up

For each unquoted key name, the extension:

1. Converts the name to lower case. With `camel_case: true`, it instead inserts
   a hyphen before each capital letter that follows another character and then
   lowers it, so `PageUp` becomes `page-up` and `pageUp` becomes `page-up`.
2. Replaces an alias with its key name, for example `ctrl` with `control`.
3. Looks the key name up in the key list, merged with your `key_map`.

If any key of a group is not found, the whole group is left as plain text. For
example, `++ctrl+foo++` stays `++ctrl+foo++` in the output, and without
`camel_case`, `++PageUp++` stays as it is, because `pageup` is not a key name.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `separator` | str | `"+"` | Text placed between keys, inside `<span>`. An empty string leaves the separator out. |
| `strict` | bool | `false` | `false`: wrap the group in `<span>`. `true`: wrap it in `<kbd>`, which follows the HTML5 rule for nested keyboard input. |
| `class` | str | `"keys"` | Class(es) of the outer element, separated by spaces. |
| `camel_case` | bool | `false` | Read `PageUp` as `page-up`. |
| `key_map` | dict | `{}` | Extra keys, or new displayed text for existing keys: `{"name": "Displayed text"}`. |

### `strict` and `separator`

With `strict: true` and `separator: ""`:

```markdown
Press ++ctrl+s++.
```

```html
<p>Press <kbd class="keys"><kbd class="key-control">Ctrl</kbd><kbd class="key-s">S</kbd></kbd>.</p>
```

With `separator: " + "` and `class: "keys shortcut"`:

```markdown
Press ++ctrl+alt+del++.
```

```html
<p>Press <span class="keys shortcut"><kbd class="key-control">Ctrl</kbd><span> + </span><kbd class="key-alt">Alt</kbd><span> + </span><kbd class="key-delete">Del</kbd></span>.</p>
```

### `key_map`

With `key_map: {hyper: Hyper}`:

```markdown
Press ++hyper+s++.
```

```html
<p>Press <span class="keys"><kbd class="key-hyper">Hyper</kbd><span>+</span><kbd class="key-s">S</kbd></span>.</p>
```

Aliases are applied before `key_map` is consulted. A `key_map` entry for an
alias name, such as `ctrl`, has no effect; use the key name, `control`.

## The `kbd` alias

`mdx_steroids.kbd` re-exports everything from `mdx_steroids.keys`. Loading
either name gives the same extension with the same options:

```python
markdown.markdown("Press ++ctrl+s++.", extensions=["mdx_steroids.kbd"])
```

## Styling

The extension only produces markup. Style it with CSS, for example:

```css
.keys kbd {
  border: 1px solid #d1d5da;
  border-radius: 3px;
  box-shadow: inset 0 -1px 0 #d1d5da;
  padding: 0.2em 0.4em;
  font-family: monospace;
}
```

Each key also has its own class, such as `.key-control` or `.key-enter`, if you
want to show icons for some keys.

## Use with other extensions

- Do not load `pymdownx.keys` together with this extension. Both use the
  `++…++` syntax and register their inline pattern under the same name, `keys`,
  so only one of them takes effect.
- [`translate_no`](translate_no.md) marks `<kbd>` elements by default, so
  browser translation leaves key names alone.

## Configuration examples

MkDocs:

```yaml
markdown_extensions:
  - mdx_steroids.keys:
      camel_case: true
      separator: " + "
```

Python:

```python
import markdown

html = markdown.markdown(
    "Press ++ctrl+s++.",
    extensions=["mdx_steroids.keys"],
    extension_configs={"mdx_steroids.keys": {"strict": True}},
)
```
