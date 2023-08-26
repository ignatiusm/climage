import pytest
from fastapi.testclient import TestClient
from imadj.server import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "I'm fine, thanks for asking!"}


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
def test_create_item(rotation, mock_infile, mock_outfile, request):
    response = client.post(
        f"/api/adjust_image/?rotate={rotation}",
        files={
            "infile": (mock_infile, request.getfixturevalue(mock_infile), "image/bmp")
        },
    )
    assert response.status_code == 200
    assert response.content == request.getfixturevalue(mock_outfile)
