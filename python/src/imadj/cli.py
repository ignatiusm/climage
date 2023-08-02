from enum import Enum

import typer
from typing_extensions import Annotated

from .helpers import le_bytes_to_int

OFFSET = (10, 14)
WIDTH = (18, 22)
HEIGHT = (22, 26)

app = typer.Typer(
    help="""
    imadj is short for IMage ADJust.\n\nimadj is a utility that allows you to
    rotate a windows bitmap image file 90 degrees to the right.
    """
)


class Rotation(str, Enum):
    left = "left"
    right = "right"
    half = "half"


class Flip(str, Enum):
    horizontal = "horizontal"
    vertical = "vertical"


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
    tpixels = []  # TODO: currently only 24 colour depth
    for ty in range(width):  # TODO need to adjust bmp header for non-square files
        for tx in range(height):
            if rotation == "right":
                sy = tx
                sx = width - ty - 1
                n = (bits_per_pixel // 8) * (sy * width + sx)
                tpixels.append(spixels[n : n + (bits_per_pixel // 8)])
            elif rotation == "left":
                sx = ty
                sy = width - tx - 1
                n = (bits_per_pixel // 8) * (sy * height + sx)
                tpixels.append(spixels[n : n + (bits_per_pixel // 8)])
            elif rotation == "half":
                sx = width - tx - 1
                # probably should be height, but we're just dealing with
                # square images at the moment
                sy = width - ty - 1
                n = (bits_per_pixel // 8) * (sy * width + sx)
                tpixels.append(spixels[n : n + (bits_per_pixel // 8)])
    return tpixels


def rotate_bmp(data, rotation):
    source_pixels, offset, width, height, bits_per_pixel = parse_file(data)
    # TODO add rotate.value, flip.value parameters
    new_header = adjust_header(data, offset, rotation)
    target_pixels = adjust_pixels(
        source_pixels, width, height, bits_per_pixel, rotation
    )
    return target_pixels, new_header


@app.command()
def cli(
    infile: Annotated[
        str,
        typer.Argument(
            help="Filename (including path) of input image file",
            show_default=False,
            envvar="INFILE",
        ),
    ],
    outfile: Annotated[
        str,
        typer.Argument(
            help="Filename (including destination path) for resulting output file",
            show_default=False,
            envvar="OUTFILE",
        ),
    ],
    rotate: Annotated[Rotation, typer.Option(case_sensitive=False)],
    # flip: Annotated[Flip, typer.Option(case_sensitive=False)],
):
    """ """
    # TODO add test to check if infile and outfile are identical and warn
    # (allow interactivity?)

    with open(infile, "rb") as f:
        data = f.read()

    # Test if file is .bmp
    assert data[:2] == b"BM"

    adjusted_pixels, new_header = rotate_bmp(data, rotate.value)

    with open(outfile, "wb") as f:
        f.write(new_header)
        f.write(b"".join(adjusted_pixels))

    print(f"{infile} rotated {rotate.value} and saved as {outfile}")


if __name__ == "__main__":
    app()
