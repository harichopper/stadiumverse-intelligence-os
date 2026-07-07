"""
Tests: Digital Fan Twin endpoints
"""

from .conftest import make_fan


class TestListFans:
    def test_empty_returns_empty_list(self, client):
        r = client.get("/api/stadium/fans")
        assert r.status_code == 200
        assert r.json()["fans"] == []

    def test_returns_seeded_fans(self, client, db):
        make_fan(db, "F001", "Carlos M.", "BRA")
        make_fan(db, "F002", "Diego R.", "ARG")
        r = client.get("/api/stadium/fans")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 2
        assert len(data["fans"]) == 2

    def test_limit_parameter(self, client, db):
        for i in range(5):
            make_fan(db, f"F{i:03d}", f"Fan {i}", "BRA")
        r = client.get("/api/stadium/fans?limit=3")
        assert r.status_code == 200
        assert len(r.json()["fans"]) == 3

    def test_fan_fields_present(self, client, db):
        make_fan(db, "F001", "Test Fan", "BRA", stress=45)
        fan = client.get("/api/stadium/fans").json()["fans"][0]
        required = [
            "id",
            "fan_id",
            "name",
            "country",
            "stress_level",
            "excitement_level",
            "current_emotion",
            "prediction_confidence",
        ]
        for field in required:
            assert field in fan, f"Missing field: {field}"

    def test_stress_level_in_valid_range(self, client, db):
        make_fan(db, "F001", "Fan", "BRA", stress=75)
        fan = client.get("/api/stadium/fans").json()["fans"][0]
        assert 0 <= fan["stress_level"] <= 100


class TestGetFanById:
    def test_get_by_fan_id(self, client, db):
        make_fan(db, "F042", "Yuki T.", "JPN")
        r = client.get("/api/stadium/fans/F042")
        assert r.status_code == 200
        assert r.json()["fan_id"] == "F042"

    def test_returns_404_for_unknown_fan(self, client):
        r = client.get("/api/stadium/fans/UNKNOWN999")
        assert r.status_code == 404

    def test_get_by_uuid(self, client, db):
        fan = make_fan(db, "F001", "Hans K.", "DEU")
        r = client.get(f"/api/stadium/fans/{fan.id}")
        assert r.status_code == 200
        assert r.json()["name"] == "Hans K."


class TestFanStressUpdate:
    def test_update_stress(self, client, db):
        make_fan(db, "F001", "Fan", "BRA", stress=30)
        r = client.patch("/api/stadium/fans/F001/stress?stress=75")
        assert r.status_code == 200
        assert r.json()["stress_level"] == 75

    def test_stress_clamps_at_100(self, client, db):
        make_fan(db, "F001", "Fan", "BRA", stress=30)
        r = client.patch("/api/stadium/fans/F001/stress?stress=150")
        assert r.status_code == 200
        assert r.json()["stress_level"] == 100

    def test_stress_clamps_at_0(self, client, db):
        make_fan(db, "F001", "Fan", "BRA", stress=50)
        r = client.patch("/api/stadium/fans/F001/stress?stress=-20")
        assert r.status_code == 200
        assert r.json()["stress_level"] == 0

    def test_update_stress_404_unknown(self, client):
        r = client.patch("/api/stadium/fans/NOBODY/stress?stress=50")
        assert r.status_code == 404
