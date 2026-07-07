"""
Tests: Volunteer endpoints
"""

from .conftest import make_volunteer


class TestListVolunteers:
    def test_empty_list(self, client):
        r = client.get("/api/stadium/volunteers")
        assert r.status_code == 200
        assert r.json()["volunteers"] == []

    def test_returns_all_volunteers(self, client, db):
        make_volunteer(db, "V001", "Alice", "available")
        make_volunteer(db, "V002", "Bob", "busy")
        r = client.get("/api/stadium/volunteers")
        assert r.status_code == 200
        assert r.json()["total"] == 2

    def test_available_only_filter(self, client, db):
        make_volunteer(db, "V001", "Alice", "available")
        make_volunteer(db, "V002", "Bob", "busy")
        r = client.get("/api/stadium/volunteers?available_only=true")
        assert r.status_code == 200
        vols = r.json()["volunteers"]
        assert all(v["availability"] == "available" for v in vols)
        assert len(vols) == 1

    def test_volunteer_fields(self, client, db):
        make_volunteer(db, "V001", "Alice")
        vol = client.get("/api/stadium/volunteers").json()["volunteers"][0]
        for field in [
            "id",
            "volunteer_id",
            "name",
            "availability",
            "skills",
            "languages",
        ]:
            assert field in vol


class TestDeployVolunteer:
    def test_deploy_available_volunteer(self, client, db):
        make_volunteer(db, "V001", "Alice", "available")
        r = client.post("/api/stadium/volunteers/V001/deploy?zone=Gate B")
        assert r.status_code == 200
        data = r.json()
        assert data["deployed"] is True
        assert data["volunteer"]["availability"] == "busy"

    def test_deploy_sets_zone_assignment(self, client, db):
        make_volunteer(db, "V001", "Alice", "available")
        r = client.post("/api/stadium/volunteers/V001/deploy?zone=Medical Zone A")
        assert r.status_code == 200
        data = r.json()
        assert data["volunteer"]["zone_assignment"] == "Medical Zone A"

    def test_deploy_creates_task(self, client, db):
        from app.db_models import VolunteerTask

        make_volunteer(db, "V001", "Alice", "available")
        r = client.post("/api/stadium/volunteers/V001/deploy?zone=Gate B")
        assert r.status_code == 200
        tasks = db.query(VolunteerTask).all()
        assert len(tasks) == 1
        assert tasks[0].title == "Deployed to Gate B"
        assert tasks[0].status == "in_progress"
        assert tasks[0].assigned_by_ai is True

    def test_deploy_unknown_volunteer(self, client):
        r = client.post("/api/stadium/volunteers/UNKNOWN/deploy?zone=Gate B")
        assert r.status_code == 404

    def test_deploy_busy_volunteer(self, client, db):
        make_volunteer(db, "V001", "Alice", "busy")
        r = client.post("/api/stadium/volunteers/V001/deploy?zone=Gate C")
        assert (
            r.status_code == 200
        )  # Wait, does the current code allow deploying busy volunteers? Let's check stadium_routes.py!
