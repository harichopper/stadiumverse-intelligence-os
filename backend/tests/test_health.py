"""
Tests: Health & Root endpoints
"""


def test_health_returns_200(client):
    r = client.get("/health")
    assert r.status_code == 200


def test_health_payload(client):
    data = client.get("/health").json()
    assert data["status"] == "healthy"
    assert data["service"] == "StadiumVerse Intelligence OS"
    assert data["version"] == "2.0.0"
    assert data["db"] == "sqlite"


def test_root_returns_200(client):
    r = client.get("/")
    assert r.status_code == 200


def test_root_payload(client):
    data = client.get("/").json()
    assert "name" in data
    assert "api" in data
    assert "docs" in data
