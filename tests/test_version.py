# this_file: tests/test_version.py
from mdx_steroids import __version__


def test_version_import():
    """Test that version can be imported from package."""
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_version_format():
    """Test that version follows an expected format."""
    assert "." in __version__
