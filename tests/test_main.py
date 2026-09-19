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

    data = response.json()

    assert data["version"] == release["version"]
    assert data["environment"] == release["environment"]
    assert data["status"] == release["status"]
    assert "id" in data

def test_created_release_appears_in_get():
    release = {
        "version": "2.0.0",
        "environment": "staging",
        "status": "pending"
    }

    create_response = client.post("/releases", json=release)

    assert create_response.status_code == 200

    created = create_response.json()

    response = client.get("/releases")

    assert response.status_code == 200

    releases = response.json()

    assert any(
        item["id"] == created["id"]
        and item["version"] == release["version"]
        and item["environment"] == release["environment"]
        and item["status"] == release["status"]
        for item in releases
    )
    
def test_create_release_invalid():
    release = {
        "version": "1.0.0",
        "environment": "production"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 422