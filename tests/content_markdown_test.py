from docgen.content.markdown import extract_title


def test_extract_title():
    expected = ("Title", "foobar")
    assert expected == extract_title("# Title\n\nfoobar")
    assert expected == extract_title("Title\n======\n\nfoobar")
