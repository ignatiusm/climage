# Tests for helper functions
from imadj.helpers import le


def test_le():
    assert le(b"\x00\x10") == 4096


def test_not_be():
    assert le(b"\x00\x10") != 16
