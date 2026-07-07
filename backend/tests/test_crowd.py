"""
Tests: Crowd Snapshot endpoints
"""

from .conftest import make_snapshot


class TestCurrentCrowd:
    def test_no_snapshot_returns_message(self, client):
        r = client.get("/api/stadium/crowd/current")
        assert r.status_code == 200
        assert "message" in r.json() or "total_fans" in r.json()

    def test_returns_latest_snapshot(self, client, db):
        make_snapshot(db, total_fans=87000)
        make_snapshot(db, total_fans=87500)
        r = client.get("/api/stadium/crowd/current")
        assert r.status_code == 200
        assert r.json()["total_fans"] == 87500

    def test_snapshot_fields_present(self, client, db):
        make_snapshot(db)
        snap = client.get("/api/stadium/crowd/current").json()
        for field in [
            "total_fans",
            "avg_stress",
            "avg_excitement",
            "risk_level",
            "gate_densities",
            "queue_avg_min",
            "weather",
        ]:
            assert field in snap

    def test_gate_densities_structure(self, client, db):
        make_snapshot(db)
        snap = client.get("/api/stadium/crowd/current").json()
        gates = snap["gate_densities"]
        for gate in ["A", "B", "C", "D"]:
            assert gate in gates
            assert 0 <= gates[gate] <= 100

    def test_risk_level_valid_value(self, client, db):
        make_snapshot(db, risk="warning")
        snap = client.get("/api/stadium/crowd/current").json()
        assert snap["risk_level"] in ["healthy", "warning", "critical"]


class TestCrowdHistory:
    def test_empty_history(self, client):
        r = client.get("/api/stadium/crowd/history?minutes=90")
        assert r.status_code == 200
        assert r.json()["snapshots"] == []

    def test_returns_within_time_window(self, client, db):
        make_snapshot(db)
        make_snapshot(db)
        r = client.get("/api/stadium/crowd/history?minutes=90")
        assert r.status_code == 200
        assert len(r.json()["snapshots"]) == 2

    def test_history_ordered_by_time(self, client, db):
        make_snapshot(db, total_fans=80000)
        make_snapshot(db, total_fans=87000)
        snaps = client.get("/api/stadium/crowd/history").json()["snapshots"]
        assert snaps[0]["total_fans"] <= snaps[-1]["total_fans"]


class TestCreateSnapshot:
    def test_post_creates_snapshot(self, client):
        r = client.post("/api/stadium/crowd/snapshot")
        assert r.status_code == 200
        data = r.json()
        assert "total_fans" in data
        assert "risk_level" in data

    def test_consecutive_snapshots_differ(self, client):
        s1 = client.post("/api/stadium/crowd/snapshot").json()
        s2 = client.post("/api/stadium/crowd/snapshot").json()
        assert s1["id"] != s2["id"]
