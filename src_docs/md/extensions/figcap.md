# figcap

`mdx_steroids.figcap` turns an image that has a title into an HTML5 `<figure>`
with the title as its `<figcaption>`. It also turns an image followed by a
definition-list caption into a figure.

The extension has no options.

## Caption from the image title

The title is the quoted text after the image path. This Markdown:

```markdown
![A cat](cat.jpg "Our office cat")

![No title](dog.jpg)
```

becomes:

```html
<p>
<figure><img alt="A cat" src="cat.jpg" title="Our office cat" /><figcaption>Our office cat</figcaption>
</figure>
</p>
<p><img alt="No title" src="dog.jpg" /></p>
```

- The image with a title is wrapped in `<figure>`, and the title is repeated in
  `<figcaption>`. The `title` attribute stays on the `<img>`.
- The image without a title is left as it is.

!!! note
    The figure stays inside the paragraph that Python-Markdown creates for the
    image, so the output has `<figure>` inside `<p>`. Browsers display this, but
    it is not valid HTML. Use the definition-list form below if you need a
    figure outside a paragraph.

### How it works

The extension registers its own inline pattern under the name `image_link`,
which replaces Python-Markdown's standard pattern for `![alt](src "title")`.
It lets the standard code build the `<img>`, then checks for a `title`. If there
is one, it returns a `<figure>` with the image and a `<figcaption>` instead of
the bare image.

Reference-style images (`![alt][ref]`) use another pattern and are not changed.

## Caption from a definition list

With Python-Markdown's `def_list` extension also loaded, write the caption as a
definition of the image:

```markdown
![A cat](cat.jpg)
:   Our office cat
```

This becomes a figure without a surrounding paragraph:

```html
<figure>
<img alt="A cat" src="cat.jpg" /><figcaption>Our office cat</figcaption>
</figure>
```

### How it works

After the document tree is built, a tree processor looks at every `<dl>`
element. It converts the list when every term (`<dt>`) contains only images and
no text, and every term is followed by exactly one definition (`<dd>`):

- A list with one image and one caption becomes one `<figure>`.
- A list with several image–caption pairs becomes a `<div>` with one
  `<figure>` per pair.
- Each `<dd>` becomes the `<figcaption>`, so the caption can contain inline
  formatting.

Any other definition list is left unchanged.

## Configuration examples

Python:

```python
import markdown

html = markdown.markdown(text, extensions=["mdx_steroids.figcap", "def_list"])
```

MkDocs:

```yaml
markdown_extensions:
  - def_list
  - mdx_steroids.figcap
```
