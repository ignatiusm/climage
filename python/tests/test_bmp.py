import pytest

from imadj import core


@pytest.fixture
def mock_bmp_square():
    with open("../data/bmp/teapot.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rotate_square_right():
    with open("../data/bmp/teapot_right.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rotate_square_left():
    with open("../data/bmp/teapot_left.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rotate_square_half():
    with open("../data/bmp/teapot_half.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rectangle():
    with open("../data/bmp/rectangle.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rotate_rectangle_right():
    with open("../data/bmp/rectangle_right.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rotate_rectangle_left():
    with open("../data/bmp/rectangle_left.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_bmp_rotate_rectangle_half():
    with open("../data/bmp/rectangle_half.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.mark.parametrize(
    "rotation, mock_infile, mock_outfile",
    [
        ("left", "mock_bmp_square", "mock_bmp_rotate_square_left"),
        ("right", "mock_bmp_square", "mock_bmp_rotate_square_right"),
        ("half", "mock_bmp_square", "mock_bmp_rotate_square_half"),
        ("left", "mock_bmp_rectangle", "mock_bmp_rotate_rectangle_left"),
        ("right", "mock_bmp_rectangle", "mock_bmp_rotate_rectangle_right"),
        ("half", "mock_bmp_rectangle", "mock_bmp_rotate_rectangle_half"),
    ],
)
def test_bmp(rotation, mock_infile, mock_outfile, request):
    assert request.getfixturevalue(mock_infile)[:2] == b"BM"
    adjusted_pixels, new_header = core.rotate_bmp(
        request.getfixturevalue(mock_infile), rotation
    )
    assert (new_header + (b"".join(adjusted_pixels))) == request.getfixturevalue(
        mock_outfile
    )
