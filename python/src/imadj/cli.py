import typer
from imadj.core import adjust_image
from imadj.helpers import RotationEnum
from typing_extensions import Annotated

app = typer.Typer(
    help="""
    imadj is short for IMage ADJust.\n\nimadj is a utility that allows you to
    rotate a windows bitmap image file 90 degrees to the right.
    """
)


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
    rotate: Annotated[RotationEnum, typer.Option(case_sensitive=False)],
    # flip: Annotated[FlipEnum, typer.Option(case_sensitive=False)],
):
    """ """
    # (allow interactivity?)
    # TODO add test to check if infile and outfile are identical and warn
    with open(infile, "rb") as f:
        data = f.read()

    with open(outfile, "wb") as f:
        f.write(adjust_image(data, rotate))

    print(f"{infile} rotated {rotate.value} and saved as {outfile}")


if __name__ == "__main__":
    app()
