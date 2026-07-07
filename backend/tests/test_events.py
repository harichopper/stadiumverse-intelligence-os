"""
Tests: Stadium Events endpoints
"""

from .conftest import make_volunteer, make_fan
from app.db_models import StadiumEvent
from datetime import datetime, timedelta


def make_event(db, event_type="goal", title="Test Goal", severity=1):
    event = StadiumEvent(
        event_type=event_type,
        title=title,
        description="Test event description",
        severity=severity,
        zone="Field",
        resolved=True,
        resolved_at=datetime.utcnow() - timedelta(minutes=5),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


class TestListEvents:
    def test_empty_events(self, client):
        r = client.get("/api/stadium/events")
        assert r.status_code == 200
        assert r.json()["events"] == []

    def test_returns_events(self, client, db):
        make_event(db, "goal", "Goal 1", 2)
        make_event(db, "crowd", "Crowd Alert", 3)
        r = client.get("/api/stadium/events")
        assert r.status_code == 200
        assert len(r.json()["events"]) == 2

    def test_limit_parameter(self, client, db):
        for i in range(10):
            make_event(db, "goal", f"Goal {i}", 1)
        r = client.get("/api/stadium/events?limit=5")
        assert r.status_code == 200
        assert len(r.json()["events"]) == 5

    def test_event_fields_present(self, client, db):
        make_event(db)
        event = client.get("/api/stadium/events").json()["events"][0]
        for field in ["id", "timestamp", "event_type", "title", "description", "severity", "zone", "resolved"]:
            assert field in event

    def test_events_ordered_newest_first(self, client, db):
        older = make_event(db, "goal", "Older Goal", 1)
        newer = make_event(db, "crowd", "Newer Alert", 3)
        events = client.get("/api/stadium/events").json()["events"]
        assert events[0]["title"] == "Newer Alert"
        assert events[1]["title"] == "Older Goal"
