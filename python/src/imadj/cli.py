from enum import Enum

import typer
from typing_extensions import Annotated

app = typer.Typer(
    help="""
    imadj is short for IMage ADJust.\n\nimadj is a utility that allows you to
    rotate a windows bitmap image file 90 degrees to the left.
    """
)


# TODO move to helpers
def le(byte_str):
    n = 0
    for index, byte in enumerate(byte_str):
        n += byte << (index * 8)
    return n


class Rotation(str, Enum):
    left = "left"
    right = "right"
    half = "half"


@app.command()
def rotate(
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
):
    """ """
    # TODO add test to check if infile and outfile are identical and warn
    # (allow interactivity?)
    if rotate.value == "left":
        with open(infile, "rb") as f:
            data = f.read()

        assert data[:2] == b"BM"
        # TODO check if these are consistent between bmp fomats
        # add height le(data[22:26])
        offset, width = le(data[10:14]), le(data[18:22])

        # Iterate in the expected order for *rotated* pixels
        # look up corresponding *source* pixel, and append to `tpixels`
        spixels = data[offset:]
        tpixels = []  # TODO: currently only BGR triples - what about alpha?
        for ty in range(width):  # TODO what should these be for non-squares?
            for tx in range(width):
                sy = tx
                sx = width - ty - 1
                n = 3 * (sy * width + sx)
                tpixels.append(spixels[n : n + 3])

        with open(outfile, "wb") as f:
            f.write(data[:offset])
            f.write(b"".join(tpixels))

        print(f"{infile} rotated left 90 degrees and saved as {outfile}")
    elif rotate.value == "right":
        print("rotate right")
    elif rotate.value == "half":
        print("rotate 180 degrees")


if __name__ == "__main__":
    app()
