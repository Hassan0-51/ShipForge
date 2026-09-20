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
    
def test_release_response_schema():
    release = {
        "version": "3.0.0",
        "environment": "production",
        "status": "deployed"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {
        "id",
        "version",
        "environment",
        "status"
    }

    assert isinstance(data["id"], int)
    assert data["version"] == "3.0.0"
    assert data["environment"] == "production"
    assert data["status"] == "deployed"
    
def test_create_release_missing_version():
    release = {
        "environment": "production",
        "status": "pending"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 422


def test_create_release_missing_environment():
    release = {
        "version": "4.0.0",
        "status": "pending"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 422


def test_create_release_missing_status():
    release = {
        "version": "4.0.0",
        "environment": "production"
    }

    response = client.post("/releases", json=release)

    assert response.status_code == 422


def test_create_release_empty_payload():
    response = client.post("/releases", json={})

    assert response.status_code == 422
    
def test_get_releases_response_schema():
    response = client.get("/releases")

    assert response.status_code == 200

    releases = response.json()

    for release in releases:
        assert set(release.keys()) == {
            "id",
            "version",
            "environment",
            "status"
        }

        assert isinstance(release["id"], int)
        assert isinstance(release["version"], str)
        assert isinstance(release["environment"], str)
        assert isinstance(release["status"], str)
        
def test_get_release_by_id():
    create_response = client.post(
        "/releases",
        json={
            "version": "2.0.0",
            "environment": "production",
            "status": "pending"
        }
    )

    release_id = create_response.json()["id"]

    response = client.get(f"/releases/{release_id}")

    assert response.status_code == 200
    assert response.json()["id"] == release_id
    assert response.json()["version"] == "2.0.0"
    assert response.json()["environment"] == "production"
    assert response.json()["status"] == "pending"
    
def test_get_release_not_found():
    response = client.get("/releases/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Release not found"