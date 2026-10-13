# img_smart

`mdx_steroids.img_smart` replaces an image that stands alone in a paragraph
with an `<img>` whose `width` and CSS classes are based on the real size of the
image file. Large images are wrapped in a link for a lightbox script. The
extension can also rewrite the image path, add `loading="lazy"`, turn the alt
text into a caption and cache image sizes in a JSON file.

## Example

Take a PNG image, `img/wide.png`, that is 1200 × 300 pixels, and these options:

```yaml
lazy: true
alt_figure: true
cache: cache.json
```

This Markdown:

```markdown
![Wide image](img/wide.png)
```

becomes:

```html
<figure><a class="fancybox" data-caption="Wide image" data-fancybox="help" href="img/wide.png"><img alt="Wide image" class="image iml" loading="lazy" src="img/wide.png" width="600" /></a><figcaption>Wide image</figcaption>
</figure>
```

While it works, the extension prints `Analyzing image: img/wide.png with size 1127`
to standard output, and it writes this to `cache.json`:

```json
{"img/wide.png": {"media": "img", "width": 1200, "height": 300}}
```

What happened:

1. The extension read the file and found a width of 1200 pixels.
2. It divided the width by the default scale of 2 and set `width="600"`.
3. 600 is more than 500, so it added the class `iml` and wrapped the image in a
   lightbox link.
4. `lazy: true` added `loading="lazy"`.
5. `alt_figure: true` wrapped everything in a `<figure>` with the alt text as
   caption.

## Which images it handles

The extension is a block processor. It handles a block only when the whole
block is one line that contains nothing but an image, optionally followed by an
attribute list:

```markdown
![Alt text](path/to/image.png)
![Alt text](path/to/image.png){: width=400 .shadow }
```

Images inside running text, and blocks with more than one line, are left to
Python-Markdown. The resulting element is added directly to the document, not
inside a `<p>`.

## Size, scale and classes

### Reading the size

The extension looks up the size in this order:

1. In the cache, if `cache` names a JSON file and the file has an entry for the
   image path.
2. From the file itself. A path that starts with `http` is downloaded with
   `requests`. Any other path is opened as a local file, relative to the
   current working directory. If the file does not exist, the size is unknown.

Then it decides what the file is:

- If it contains `<svg` and `</svg>`, it is an SVG. The size comes from the
  `viewBox` attribute.
- If it contains `<html` and `</html>`, it prints
  `WARNING: <path> is of type HTML, possibly 404` and the size is unknown.
- Otherwise `filetype` guesses the type. Images are measured with `imageio`;
  videos are measured with `imageio`'s `pyav` plugin, which needs the separate
  `av` package.

If the size is larger than 1920 × 1080, it is scaled down proportionally to fit
1920 × 1080.

### Scale

The displayed width is the image width divided by a scale. The default scale is
`2`, which suits images saved at double resolution. The scale changes when the
attribute list contains:

| Attribute | Effect |
|---|---|
| `width=N` | The width becomes `N` and the scale becomes `1` |
| `height=N` | The height becomes `N` |
| `.lores` (class) | The scale becomes `1` |
| `data-scale=N%` | The scale becomes `100 / N`; `data-scale=25%` gives `4`, so a 1200-pixel image gets `width="300"` |

`data-scale` is not copied to the HTML. All other attributes and classes in the
list are copied to the `<img>`; a `width` you set is then replaced by the
computed width.

### Width and classes

Every image gets the class `image`. The extension then compares the displayed
width (`width / scale`):

| Displayed width | `width` attribute | Extra class | Lightbox link |
|---|---|---|---|
| More than 1280 | displayed width | `imxl` | yes |
| 501 to 1280 | displayed width | `iml` | yes |
| 33 to 500 | displayed width | `imm` | no |
| 1 to 32 (image width not 0) | image width | `ims` | no |
| Size unknown | none | none | no |

The lightbox link is `<a class="fancybox" data-fancybox="help" href="…">` with a
`data-caption` taken from the image title, or from the alt text if there is no
title. It works with the [Fancybox](https://fancyapps.com/fancybox/) script,
which you add to the page yourself.

The image title (`![alt](src "title")`) is not written to the `<img>`. It is
only used for `data-caption`.

### Examples of sizes

| Markdown | File size | Result |
|---|---|---|
| `![Small image](img/small.png)` | 200 × 100 | `<img alt="Small image" class="image imm" src="img/small.png" width="100" />` |
| `![Sized](img/wide.png){: width=400 .shadow }` | 1200 × 300 | `<img alt="Sized" class="shadow image imm" src="img/wide.png" width="400" />` |
| `![Missing](nope.png)` | file not found | `<img alt="Missing" class="image" src="nope.png" />` |

## Rewriting the path

`find`, `repl_path` and `repl_url` let the path in the Markdown differ from
both the file on disk and the URL in the HTML:

- `find` is the text to look for in the image path.
- `repl_path` replaces `find` to get the local file path to measure.
- `repl_url` replaces `find` to get the `src` written to the HTML.

With `find: /media/`, `repl_path: img/` and
`repl_url: https://cdn.example.com/img/`:

```markdown
![Shot](/media/small.png)
```

The extension measures `img/small.png` and writes:

```html
<img alt="Shot" class="image imm" src="https://cdn.example.com/img/small.png" width="100" />
```

The cache uses the local file path (after `repl_path`) as its key.

## Options

| Option | Type | Default | Meaning |
|---|---|---|---|
| `find` | str | `""` | Text to replace in the image path. Nothing is replaced when empty. |
| `repl_path` | str | `""` | Replacement for `find` when building the local file path. |
| `repl_url` | str | `""` | Replacement for `find` when building the `src` URL. |
| `alt_figure` | bool | `false` | Wrap the result in `<figure>` with the alt text as `<figcaption>`. |
| `cache` | str | `""` | Path of a JSON file that stores image sizes between runs. The file is read and rewritten for every handled image. |
| `lazy` | bool | `false` | Add `loading="lazy"` to the `<img>`. |

## Configuration example

MkDocs:

```yaml
markdown_extensions:
  - attr_list
  - mdx_steroids.img_smart:
      find: /media/
      repl_path: src_docs/md/media/
      repl_url: /media/
      cache: .img_cache.json
      lazy: true
```

## Limitations

- The extension prints progress messages with `print()`, not through logging.
- Only images whose size is known are written to the cache.
- A failed download is ignored silently; the image then has no size.
