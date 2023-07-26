from os import remove

from imadj.cli import app
from typer.testing import CliRunner

runner = CliRunner()


def file_contents_are_identical(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        contents1 = f1.read()
        contents2 = f2.read()
    return contents1 == contents2


def test_cli():
    INFILE = "tests/teapot_original.bmp"
    OUTFILE = "tests/cli_result.bmp"
    TESTFILE = "tests/teapot_right.bmp"
    result = runner.invoke(app, [INFILE, OUTFILE, "--rotate", "right"])
    assert result.exit_code == 0
    assert f"{INFILE} rotated right 90 degrees and saved as {OUTFILE}" in result.stdout
    assert file_contents_are_identical(TESTFILE, OUTFILE)
    remove(OUTFILE)
