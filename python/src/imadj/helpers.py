# Helper functions
from enum import Enum


class RotationEnum(str, Enum):
    left = "left"
    right = "right"
    half = "half"


class FlipEnum(str, Enum):
    horizontal = "horizontal"
    vertical = "vertical"


def le_bytes_to_int(byte_str):
    """
    Converts a LITTLE ENDIAN bytestring into an integer
    """
    n = 0
    for index, byte in enumerate(byte_str):
        n += byte << (index * 8)
    return n
