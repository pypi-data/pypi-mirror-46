import pytest

from sparrow.src.helper import extract_info


def test_extract_triggers():
    test = [[1, 2], [3], [4, 5, [1, 100, [
        10, 50, 100, 1000
    ]]], 10, 10]
    assert extract_info(test) == [1, 2, 3, 4, 5, 100, 10, 50, 1000]