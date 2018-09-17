from unittest import mock
import pytest

from multidocs.content.utils import transform_url


@pytest.mark.parametrize(
    "url,path,expect",
    (
        ("example.md", "foo.md", "example.html"),
        ("../example.md", "foo/bar.md", "../example.html"),
        ("../../example.md", "foo/bar/baz.md", "../../example.html"),
        # .md should not be converted to .html
        (
            "../example.md",
            "foo.md",
            "https://github.com/org/repo/tree/master/example.md",
        ),
        # absolute-like urls should be left alone
        ("/example.md", "foo.md", None),
        ("//example/foo.txt", "foo.md", None),
        ("https://example/foo.txt", "foo.md", None),
    ),
)
def test_relative_urls_are_converted(url, path, expect):
    if expect is None:
        expect = url
    source = mock.Mock(url="https://github.com/org/repo/tree/master/dir")
    assert expect == transform_url(url, mock.Mock(path=path, source=source))
