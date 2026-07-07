"""
Tests: Dashboard summary endpoint
"""

from .conftest import make_fan, make_volunteer, make_snapshot, make_decision


class TestDashboard:
    def test_dashboard_returns_200(self, client):
        r = client.get("/api/stadium/dashboard")
        assert r.status_code == 200

    def test_dashboard_structure(self, client):
        data = client.get("/api/stadium/dashboard").json()
        for key in [
            "crowd",
            "fans_online",
            "volunteers_available",
            "recent_decisions",
            "recent_events",
            "timestamp",
        ]:
            assert key in data

    def test_fans_online_count(self, client, db):
        make_fan(db, "F001", "Fan A", "BRA")
        make_fan(db, "F002", "Fan B", "ARG")
        data = client.get("/api/stadium/dashboard").json()
        assert data["fans_online"] == 2

    def test_volunteers_available_count(self, client, db):
        make_volunteer(db, "V001", "Alice", "available")
        make_volunteer(db, "V002", "Bob", "busy")
        data = client.get("/api/stadium/dashboard").json()
        assert data["volunteers_available"] == 1

    def test_recent_decisions_list(self, client, db):
        make_decision(db, "Coordinator", "Decision A")
        make_decision(db, "Medical", "Decision B")
        data = client.get("/api/stadium/dashboard").json()
        assert isinstance(data["recent_decisions"], list)
        assert len(data["recent_decisions"]) <= 5

    def test_crowd_data_included_when_snapshot_exists(self, client, db):
        make_snapshot(db, total_fans=87342)
        data = client.get("/api/stadium/dashboard").json()
        assert data["crowd"].get("total_fans") == 87342

    def test_timestamp_present(self, client):
        data = client.get("/api/stadium/dashboard").json()
        assert "T" in data["timestamp"]  # ISO format

    def test_dashboard_fast_response(self, client, db):
        """Dashboard must respond quickly — critical for real-time use."""
        import time

        make_snapshot(db)
        make_fan(db, "F001", "Fan", "BRA")
        start = time.time()
        client.get("/api/stadium/dashboard")
        elapsed = time.time() - start
        assert elapsed < 1.0, f"Dashboard too slow: {elapsed:.2f}s"
