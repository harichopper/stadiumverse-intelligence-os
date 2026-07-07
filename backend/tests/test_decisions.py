"""
Tests: AI Decision (Black Box Recorder) endpoints
"""

from .conftest import make_decision


class TestListDecisions:
    def test_empty_decisions(self, client):
        r = client.get("/api/stadium/decisions")
        assert r.status_code == 200
        assert r.json()["decisions"] == []

    def test_returns_decisions(self, client, db):
        make_decision(db, "Coordinator", "Deploy volunteers to Gate B")
        make_decision(db, "Medical", "Alert medic to Zone C")
        r = client.get("/api/stadium/decisions")
        assert r.status_code == 200
        assert len(r.json()["decisions"]) == 2

    def test_limit_parameter(self, client, db):
        for i in range(10):
            make_decision(db, "Navigation", f"Decision {i}")
        r = client.get("/api/stadium/decisions?limit=5")
        assert r.status_code == 200
        assert len(r.json()["decisions"]) == 5

    def test_decision_fields_present(self, client, db):
        make_decision(db)
        d = client.get("/api/stadium/decisions").json()["decisions"][0]
        for field in ["id", "match_minute", "agent", "decision",
                      "confidence", "outcome", "affected_fans", "impact_pct"]:
            assert field in d

    def test_decisions_ordered_newest_first(self, client, db):
        make_decision(db, confidence=0.80)
        make_decision(db, confidence=0.95)
        decisions = client.get("/api/stadium/decisions").json()["decisions"]
        assert decisions[0]["confidence"] == 0.95


class TestRecordDecision:
    def test_record_new_decision(self, client):
        r = client.post(
            "/api/stadium/decisions"
            "?agent=Coordinator"
            "&decision=Deploy+3+volunteers+to+Gate+B"
            "&confidence=0.94"
            "&match_minute=67"
            "&affected_fans=1400"
        )
        assert r.status_code == 200
        data = r.json()
        assert data["agent"] == "Coordinator"
        assert data["outcome"] == "PENDING"
        assert data["confidence"] == 0.94

    def test_default_outcome_is_pending(self, client):
        r = client.post("/api/stadium/decisions?agent=Medical&decision=Alert+Zone+D")
        assert r.status_code == 200
        assert r.json()["outcome"] == "PENDING"


class TestUpdateOutcome:
    def test_update_decision_outcome(self, client, db):
        d = make_decision(db, outcome="PENDING")
        r = client.patch(f"/api/stadium/decisions/{d.id}/outcome?outcome=SUCCESS&impact_pct=23.5")
        assert r.status_code == 200
        data = r.json()
        assert data["outcome"] == "SUCCESS"
        assert data["impact_pct"] == 23.5

    def test_update_unknown_decision(self, client):
        r = client.patch("/api/stadium/decisions/nonexistent-id/outcome?outcome=SUCCESS")
        assert r.status_code == 404

    def test_all_valid_outcomes(self, client, db):
        for outcome in ["SUCCESS", "PARTIAL", "FAILED", "PENDING"]:
            d = make_decision(db, outcome="PENDING")
            r = client.patch(f"/api/stadium/decisions/{d.id}/outcome?outcome={outcome}")
            assert r.status_code == 200
            assert r.json()["outcome"] == outcome
