# Tests for helper functions
from imadj.helpers import le_bytes_to_int


def test_le_bytes_to_int():
    assert le_bytes_to_int(b"\x00\x10") == 4096


def test_le_bytes_to_int_is_not_be():
    assert le_bytes_to_int(b"\x00\x10") != 16
