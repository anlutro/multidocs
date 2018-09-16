from docgen.content import guess_file_title


def test_guess_file_title():
    assert "Some test file" == guess_file_title("some-test-file.md")
