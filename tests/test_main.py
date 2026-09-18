from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["application"] == "ShipForge"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_releases():
    response = client.get("/releases")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_create_release():
    release = {
        "version": "1.0.0",
        "environment": "production",
        "status": "pending"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 200
    assert response.json() == release
    
def test_create_release_invalid():
    release = {
        "version": "1.0.0",
        "environment": "production"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 422