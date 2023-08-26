import pytest


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
