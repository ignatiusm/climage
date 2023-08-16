from enum import Enum

import typer
from typing_extensions import Annotated

from .bmp import rotate_bmp

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
