from enum import Enum

import typer
from typing_extensions import Annotated

from .helpers import le_bytes_to_int

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
# add height le_bytes_to_int(data[22:26])
def parse_header(data: bytes) -> (bytes, int, int):
    offset, width = le_bytes_to_int(data[10:14]), le_bytes_to_int(data[18:22])
    spixels = data[offset:]
    return spixels, offset, width


def adjust_bytes(spixels: bytes, width: int) -> bytes:
    # Iterate in the expected order for *rotated* pixels
    # look up corresponding *source* pixel, and append to `tpixels`
    tpixels = []  # TODO: currently only BGR triples - what about alpha?
    for ty in range(width):  # TODO what should these be for non-squares?
        for tx in range(width):
            sy = tx
            sx = width - ty - 1
            n = 3 * (sy * width + sx)
            tpixels.append(spixels[n : n + 3])
    return tpixels


def rotate_right(data):
    source_pixels, offset, width = parse_header(data)
    # TODO add rotate.value, flip.value parameters
    target_pixels = adjust_bytes(source_pixels, width)
    return target_pixels, offset


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

    assert data[:2] == b"BM"

    adjusted_pixels, offset = rotate_right(data)

    with open(outfile, "wb") as f:
        f.write(data[:offset])
        f.write(b"".join(adjusted_pixels))

    print(f"{infile} rotated right 90 degrees and saved as {outfile}")


if __name__ == "__main__":
    app()
