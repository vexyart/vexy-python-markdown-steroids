# this_file: mdx_steroids/figcap.py
r"""
Figure Caption Extension for Python-Markdown
==================================

Converts \![alttext](http://example.com/image.png "caption")
to the image with a caption.
Its syntax is same as embedding images.

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

"""

from markdown import Extension
import xml.etree.ElementTree as etree

from markdown.inlinepatterns import IMAGE_LINK_RE, ImageInlineProcessor
from markdown.treeprocessors import Treeprocessor


class FigureCaptionExtension(Extension):
    def extendMarkdown(self, md):
        # append to inline patterns
        md.inlinePatterns.register(FigureCaptionPattern(IMAGE_LINK_RE, md), "image_link", 150)
        md.treeprocessors.register(DefinitionCaptionProcessor(md), "definition_caption", 6)


class FigureCaptionPattern(ImageInlineProcessor):
    def handleMatch(self, m, data):
        image, start, end = super().handleMatch(m, data)
        if image is None:
            return image, start, end
        title = image.get("title")
        if title:
            figure = etree.Element("figure")
            figure.append(image)
            etree.SubElement(figure, "figcaption").text = title
            return figure, start, end
        else:
            return image, start, end


def makeExtension(*args, **kwargs):
    return FigureCaptionExtension(*args, **kwargs)


class DefinitionCaptionProcessor(Treeprocessor):
    """Preserve the manuals' image followed by a definition-list caption syntax."""

    def run(self, root):
        for node in list(root.iter("dl")):
            children = list(node)
            if not children or len(children) % 2:
                continue
            pairs = list(zip(children[::2], children[1::2]))
            if not all(self.is_image_caption(term, definition) for term, definition in pairs):
                continue
            node.tag = "figure" if len(pairs) == 1 else "div"
            for child in children:
                node.remove(child)
            for term, definition in pairs:
                figure = node if len(pairs) == 1 else etree.SubElement(node, "figure")
                for image in list(term):
                    figure.append(image)
                definition.tag = "figcaption"
                figure.append(definition)
        return root

    @staticmethod
    def is_image_caption(term, definition):
        return (term.tag == "dt" and definition.tag == "dd" and len(term) > 0
                and not (term.text or "").strip()
                and all(image.tag == "img" and not (image.tail or "").strip() for image in term))
