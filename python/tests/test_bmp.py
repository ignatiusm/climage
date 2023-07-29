import pytest

from imadj import cli


@pytest.fixture
def mock_original_bmp_image():
    with open("tests/teapot_original.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_rotate_right_bmp_image():
    with open("tests/teapot_right.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_rotate_left_bmp_image():
    with open("tests/teapot_left.bmp", "rb") as f:
        data = f.read()
    return data


@pytest.fixture
def mock_rotate_half_bmp_image():
    with open("tests/teapot_half.bmp", "rb") as f:
        data = f.read()
    return data


def test_rotate_right_is_equal_to_example(
    mock_original_bmp_image, mock_rotate_right_bmp_image, rotation="right"
):
    assert mock_original_bmp_image[:2] == b"BM"
    adjusted_pixels, offset = cli.rotate_bmp(mock_original_bmp_image, rotation)
    assert (
        mock_original_bmp_image[:offset] + (b"".join(adjusted_pixels))
    ) == mock_rotate_right_bmp_image


def test_rotate_left_is_equal_to_example(
    mock_original_bmp_image, mock_rotate_left_bmp_image, rotation="left"
):
    assert mock_original_bmp_image[:2] == b"BM"
    adjusted_pixels, offset = cli.rotate_bmp(mock_original_bmp_image, rotation)
    assert (
        mock_original_bmp_image[:offset] + (b"".join(adjusted_pixels))
    ) == mock_rotate_left_bmp_image


def test_rotate_half_is_equal_to_example(
    mock_original_bmp_image, mock_rotate_half_bmp_image, rotation="half"
):
    assert mock_original_bmp_image[:2] == b"BM"
    adjusted_pixels, offset = cli.rotate_bmp(mock_original_bmp_image, rotation)
    assert (
        mock_original_bmp_image[:offset] + (b"".join(adjusted_pixels))
    ) == mock_rotate_half_bmp_image
