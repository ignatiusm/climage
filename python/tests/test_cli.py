from os import remove

import pytest
from imadj.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def file_contents_are_identical(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        contents1 = f1.read()
        contents2 = f2.read()
    return contents1 == contents2


@pytest.mark.parametrize(
    "rotation, infile, outfile",
    [
        ("left", "../data/bmp/teapot.bmp", "../data/bmp/teapot_left.bmp"),
        ("right", "../data/bmp/teapot.bmp", "../data/bmp/teapot_right.bmp"),
        ("half", "../data/bmp/teapot.bmp", "../data/bmp/teapot_half.bmp"),
        ("left", "../data/bmp/rectangle.bmp", "../data/bmp/rectangle_left.bmp"),
        ("right", "../data/bmp/rectangle.bmp", "../data/bmp/rectangle_right.bmp"),
        ("half", "../data/bmp/rectangle.bmp", "../data/bmp/rectangle_half.bmp"),
    ],
)
def test_cli(rotation, infile, outfile):
    INFILE = infile
    OUTFILE = "../data/bmp/cli_result.bmp"
    TESTFILE = outfile
    result = runner.invoke(app, [INFILE, OUTFILE, "--rotate", rotation])
    assert result.exit_code == 0
    assert f"{INFILE} rotated {rotation} and saved as {OUTFILE}" in result.stdout
    assert file_contents_are_identical(TESTFILE, OUTFILE)
    remove(OUTFILE)
