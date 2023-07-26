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


def test_rotate_right_is_equal_to_example(
    mock_original_bmp_image, mock_rotate_right_bmp_image
):
    assert mock_original_bmp_image[:2] == b"BM"
    adjusted_pixels, offset = cli.rotate_right(mock_original_bmp_image)
    assert (
        mock_original_bmp_image[:offset] + (b"".join(adjusted_pixels))
    ) == mock_rotate_right_bmp_image
