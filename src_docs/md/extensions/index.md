# Extensions overview

All extensions live in the `mdx_steroids` package. Load an extension by its
dotted name, for example `mdx_steroids.figcap`.

## By task

### Images

| Task | Extension |
|---|---|
| Serve images from another host or a CDN | [`absimgsrc`](absimgsrc.md) |
| Change part of every image path | [`replimgsrc`](replimgsrc.md) |
| Show the image title as a caption | [`figcap`](figcap.md) |
| Set image widths from the real image size, add lightbox links | [`img_smart`](img_smart.md) |

### Links

| Task | Extension |
|---|---|
| Write `[[Page Name]]` links | [`wikilink`](wikilink.md) |
| Write short internal links such as `[Setup](setup)` | [`interlink`](interlink.md) |

### Text and markup

| Task | Extension |
|---|---|
| Show keyboard shortcuts | [`keys`](keys.md) |
| Keep notes in the source that never reach the HTML | [`comments`](comments.md) |
| Read YAML front matter | [`meta_yaml`](meta_yaml.md) |
| Use variables, loops and includes | [`md_mako`](md_mako.md) |

### HTML clean-up

| Task | Extension |
|---|---|
| Remove elements by selector, and remove empty elements | [`kill_tags`](kill_tags.md) |
| Stop browser translation of code and key names | [`translate_no`](translate_no.md) |

## Module names

| Load as | Module file | Extension class |
|---|---|---|
| `mdx_steroids.absimgsrc` | `absimgsrc.py` | `MDXAbsoluteImagesExtension` |
| `mdx_steroids.comments` | `comments.py` | `CommentsExtension` |
| `mdx_steroids.figcap` | `figcap.py` | `FigureCaptionExtension` |
| `mdx_steroids.img_smart` | `img_smart.py` | `MDXSmartImageExtension` |
| `mdx_steroids.interlink` | `interlink.py` | `MDXInterLinkExtension` |
| `mdx_steroids.keys` | `keys.py` | `KeysExtension` |
| `mdx_steroids.kbd` | `kbd.py` (re-exports `keys`) | `KeysExtension` |
| `mdx_steroids.kill_tags` | `kill_tags.py` | `KillTagsExtension` |
| `mdx_steroids.md_mako` | `md_mako.py` | `MarkdownMakoExtension` |
| `mdx_steroids.meta_yaml` | `meta_yaml.py` | `MetaYamlExtension` |
| `mdx_steroids.replimgsrc` | `replimgsrc.py` | `MDXReplaceImageSrcExtension` |
| `mdx_steroids.translate_no` | `translate_no.py` | `NoTranslateExtensions` |
| `mdx_steroids.wikilink` | `wikilink.py` | `WikiLinkExtension` |

`keymap_db.py` is not an extension. It holds the key names that `keys` uses.

## Origins

Most extensions are by Adam Twardoch. Some are forks:

- `keys` is a fork of `pymdownx.keys` by Isaac Muse, written after an idea by
  Adam Twardoch.
- `figcap` is based on `mdx_figcap` by mkszk.
- `meta_yaml` is by Bernhard Fisseni, based on the meta-data extension of
  Python-Markdown.
- `comments` is based on `python-markdown-comments` by ryneeverett.
- `wikilink` and `interlink` are adapted from the WikiLinks extension of
  Python-Markdown.
- `img_smart` is based on `micropress` by glushchenko.
