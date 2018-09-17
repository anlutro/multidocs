from unittest import mock

from multidocs.entities import Content


def test_content_is_sorted_by_path():
    c1 = Content(path="page-a", source=mock.Mock())
    c2 = Content(path="page-b", source=mock.Mock())
    assert sorted([c2, c1]) == [c1, c2]
    assert sorted([c1, c2]) == [c1, c2]


def test_content_is_sorted_by_title_over_path():
    c1 = Content(path="page-2", title="A", source=mock.Mock())
    c2 = Content(path="page-1", title="B", source=mock.Mock())
    assert sorted([c2, c1]) == [c1, c2]
    assert sorted([c1, c2]) == [c1, c2]
