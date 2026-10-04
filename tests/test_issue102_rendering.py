# this_file: tests/test_issue102_rendering.py
"""Rendering contracts used by the historical FontLab manual."""
import markdown


def test_internal_link_keeps_full_prefix_suffix_and_anchor():
    html = markdown.markdown('[Page](Page#anchor)', extensions=['mdx_steroids.interlink'], extension_configs={'mdx_steroids.interlink': {'base_url': '/manual/', 'end_url': '.md'}})
    assert 'href="/manual/Page.md#anchor"' in html


def test_image_rewrite_keeps_alt_text_and_title():
    html = markdown.markdown('![Picture](https://example.com/images/a.png "Caption")', extensions=['mdx_steroids.replimgsrc'], extension_configs={'mdx_steroids.replimgsrc': {'find': 'https://example.com/images/', 'replace': '../img/'}})
    assert 'src="../img/a.png"' in html
    assert 'alt="Picture"' in html
    assert 'title="Caption"' in html
