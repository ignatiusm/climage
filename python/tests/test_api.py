from fastapi.testclient import TestClient
from imadj.server import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "I'm fine, thanks for asking!"}


def test_create_item():
    response = client.post(
        "/api/adjust_image/?rotate=left",
        files={
            "infile": ("teapot.bmp", open("../data/bmp/teapot.bmp", "rb"), "image/bmp")
        },
    )
    assert response.status_code == 200
