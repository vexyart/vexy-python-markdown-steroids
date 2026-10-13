# vexy-python-markdown-steroids

`vexy-python-markdown-steroids` is a set of twelve extensions for
[Python-Markdown](https://python-markdown.github.io/). You install the package
from PyPI as `vexy-python-markdown-steroids`, and import the extensions from the
`mdx_steroids` package.

Each extension is a separate module. You turn it on by adding its dotted name,
such as `mdx_steroids.keys`, to the list of extensions in Python, in the
`python -m markdown` command, or in the `markdown_extensions` list of an MkDocs
site.

## One extension, from input to output

The `keys` extension turns key combinations into `<kbd>` elements. This
Markdown:

```markdown
Press ++ctrl+s++.
```

becomes this HTML with `extensions=["mdx_steroids.keys"]`:

```html
<p>Press <span class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd class="key-s">S</kbd></span>.</p>
```

The extension recognised `ctrl` as an alias of the key `control`, printed it as
`Ctrl`, and gave each key a CSS class you can style.

## The extensions

| Extension | What it does | Stage |
|---|---|---|
| [`absimgsrc`](extensions/absimgsrc.md) | Prepends a base URL to relative image paths | Tree processor |
| [`comments`](extensions/comments.md) | Removes `<!--- … -->` comments, keeps `<!-- … -->` | Preprocessor |
| [`figcap`](extensions/figcap.md) | Turns titled images into `<figure>` with `<figcaption>` | Inline pattern, tree processor |
| [`img_smart`](extensions/img_smart.md) | Reads image sizes, sets `width` and classes, adds lightbox links | Block processor |
| [`interlink`](extensions/interlink.md) | Adds a prefix and suffix to short internal link targets | Preprocessor |
| [`keys`](extensions/keys.md) (alias [`kbd`](extensions/keys.md#the-kbd-alias)) | Renders `++ctrl+s++` as `<kbd>` elements | Inline pattern |
| [`kill_tags`](extensions/kill_tags.md) | Deletes HTML elements by CSS or XPath selector, and empty elements | Postprocessor |
| [`md_mako`](extensions/md_mako.md) | Runs the Markdown through the Mako template engine | Preprocessor |
| [`meta_yaml`](extensions/meta_yaml.md) | Reads a YAML front-matter block into `md.Meta` | Preprocessor |
| [`replimgsrc`](extensions/replimgsrc.md) | Find-and-replace in image `src` attributes | Tree processor |
| [`translate_no`](extensions/translate_no.md) | Adds `translate="no"` to code, keys and other elements | Postprocessor |
| [`wikilink`](extensions/wikilink.md) | Turns `[[Page Name]]` into a Markdown link | Preprocessor |

The "Stage" column says where in the Python-Markdown pipeline the extension
works. [Architecture](development/architecture.md) explains the stages and the
order in which the extensions run.

## Where to go next

- [Installation](getting-started/installation.md)
- [Quick start](getting-started/quickstart.md): use an extension from Python,
  from the command line and from MkDocs.
- [Configuration](getting-started/configuration.md): how to pass options.
- [Extensions overview](extensions/index.md): pick the extension you need.

## License

BSD 3-Clause. Several extensions are based on code by other authors; see
[License and credits](about/license.md).
