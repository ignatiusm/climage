import math

from .helpers import le_bytes_to_int

OFFSET = (10, 14)
WIDTH = (18, 22)
HEIGHT = (22, 26)


# TODO check if these are consistent between bmp fomats
def parse_file(data: bytes) -> (bytes, int, int):
    offset, width, height, bits_per_pixel = (
        le_bytes_to_int(data[OFFSET[0] : OFFSET[1]]),
        le_bytes_to_int(data[WIDTH[0] : WIDTH[1]]),
        le_bytes_to_int(data[HEIGHT[0] : HEIGHT[1]]),
        le_bytes_to_int(data[28:30]),
    )
    spixels = data[offset:]
    return spixels, offset, width, height, bits_per_pixel


def pad_bytes(dimension: int) -> int:
    return math.ceil(dimension / 4) * 4


def adjust_header(data: bytes, offset: int, rotation: str) -> bytes:
    if rotation in "right|left":
        new_header = (
            data[: WIDTH[0]]
            + data[HEIGHT[0] : HEIGHT[1]]
            + data[WIDTH[0] : WIDTH[1]]
            + data[HEIGHT[1] : offset]
        )
    else:
        new_header = data[:offset]
    return new_header


def adjust_pixels(
    spixels: bytes,
    width: int,
    height: int,
    bits_per_pixel: int,
    rotation: str,
) -> bytes:
    # Iterate in the expected order for *rotated* pixels
    # look up corresponding *source* pixel, and append to `tpixels`
    tpixels = []
    # TODO: currently only 24 colour depth
    pixel_format = bits_per_pixel // 8
    if rotation == "right":
        for ty in range(width):
            for tx in range(height):
                sy = tx
                sx = width - ty - 1
                n = pixel_format * (sy * pad_bytes(width) + sx)
                tpixels.append(spixels[n : n + pixel_format])
                # Add padding if last pixel in row
                if tx == height - 1:
                    padding_size = (
                        pad_bytes(height * pixel_format) - height * pixel_format
                    )
                    if padding_size > 0:
                        for _ in range(padding_size):
                            tpixels.append(b"\xff")
    elif rotation == "left":
        for ty in range(width):
            for tx in range(height):
                sx = ty
                sy = height - tx - 1
                n = pixel_format * (sy * pad_bytes(width) + sx)
                tpixels.append(spixels[n : n + pixel_format])
                # Add padding if last pixel in row
                if tx == height - 1:
                    padding_size = (
                        pad_bytes(height * pixel_format) - height * pixel_format
                    )
                    if padding_size > 0:
                        for _ in range(padding_size):
                            tpixels.append(b"\xff")
    elif rotation == "half":
        for ty in range(height):
            for tx in range(width):
                sx = width - tx - 1
                sy = height - ty - 1
                n = pixel_format * (sy * pad_bytes(width) + sx)
                tpixels.append(spixels[n : n + pixel_format])
                # Add padding if last pixel in row
                if tx == width - 1:
                    padding_size = (
                        pad_bytes(width * pixel_format) - width * pixel_format
                    )
                    if padding_size > 0:
                        for _ in range(padding_size):
                            tpixels.append(b"\xff")
    return tpixels


def rotate_bmp(data, rotation):
    source_pixels, offset, width, height, bits_per_pixel = parse_file(data)
    # TODO add rotate.value, flip.value parameters
    target_pixels = adjust_pixels(
        source_pixels, width, height, bits_per_pixel, rotation
    )
    new_header = adjust_header(data, offset, rotation)
    return target_pixels, new_header
