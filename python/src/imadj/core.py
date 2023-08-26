from enum import Enum

from imadj.bmp import rotate_bmp


def adjust_image(data, rotate: Enum):
    # Test if file is .bmp
    assert data[:2] == b"BM"

    adjusted_pixels, new_header = rotate_bmp(data, rotate.value)

    return new_header + (b"".join(adjusted_pixels))
