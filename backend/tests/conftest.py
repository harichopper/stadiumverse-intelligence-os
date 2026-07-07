"""
StadiumVerse Intelligence OS — Test Configuration
Isolated in-memory SQLite, never touches stadiumverse.db.
"""

import os
os.environ["TESTING"] = "true"   # Prevents lifespan seeding real DB

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# ── Create in-memory engine FIRST, then import app ───────────────────────────
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Now import Base & models so metadata is populated
from app.database import Base, get_db  # noqa: E402
import app.db_models  # noqa: F401, E402 — Registers all ORM models on Base

# Create ALL tables in the in-memory engine once at import time
Base.metadata.create_all(bind=test_engine)

from app.main import app  # noqa: E402
from app.db_models import (  # noqa: E402
    DigitalFan, Volunteer, CrowdSnapshot,
    AIDecision, StadiumEvent, VolunteerTask,
)

# Override the DB dependency globally
def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    """Single TestClient for the whole test session."""
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Fresh database session per test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def clean_db(db: Session) -> Generator[None, None, None]:
    """Wipe all rows before every test — guarantees test isolation."""
    yield
    for model in [VolunteerTask, StadiumEvent, AIDecision,
                  CrowdSnapshot, Volunteer, DigitalFan]:
        db.query(model).delete()
    db.commit()


# ── Data factories ────────────────────────────────────────────────────────────

def make_fan(
    db: Session,
    fan_id: str = "F001",
    name: str = "Test Fan",
    country: str = "BRA",
    stress: int = 30,
    emotion: str = "excited"
) -> DigitalFan:
    """
    Create a test DigitalFan in the database.
    """
    fan = DigitalFan(
        fan_id=fan_id, name=name, country=country, flag="🇧🇷",
        sector="N1", seat="10A",
        stress_level=stress, excitement_level=70,
        hunger_level=25, fatigue_level=15,
        prediction_confidence=0.88, risk_score=max(0, stress - 30),
        current_emotion=emotion,
        current_thought="Go team!",
        memory_summary="Previous visit was great",
        predicted_action="Will stay till end",
    )
    db.add(fan)
    db.commit()
    db.refresh(fan)
    return fan


def make_volunteer(
    db: Session,
    vid: str = "V001",
    name: str = "Volunteer",
    availability: str = "available"
) -> Volunteer:
    """
    Create a test Volunteer in the database.
    """
    vol = Volunteer(
        volunteer_id=vid, name=name,
        languages="en,ar", skills="crowd_control",
        medical_training=False,
        availability=availability,
        zone_assignment="Gate B",
        loc_x=50.0, loc_y=50.0, tasks_today=0,
    )
    db.add(vol)
    db.commit()
    db.refresh(vol)
    return vol


def make_snapshot(
    db: Session,
    total_fans: int = 87342,
    risk: str = "healthy",
    gate_b: float = 88.0
) -> CrowdSnapshot:
    """
    Create a test CrowdSnapshot in the database.
    """
    snap = CrowdSnapshot(
        total_fans=total_fans, avg_stress=45.0, avg_excitement=65.0,
        risk_level=risk,
        gate_a_density=70.0, gate_b_density=gate_b,
        gate_c_density=65.0, gate_d_density=60.0,
        queue_avg_min=6.5, weather_temp=22.0, weather_rain_pct=18.0,
    )
    db.add(snap)
    db.commit()
    db.refresh(snap)
    return snap


def make_decision(
    db: Session,
    agent: str = "Coordinator",
    decision: str = "Deploy volunteers to Gate B",
    confidence: float = 0.94,
    outcome: str = "SUCCESS",
    match_minute: int = 67
) -> AIDecision:
    """
    Create a test AIDecision in the database.
    """
    d = AIDecision(
        match_minute=match_minute, agent=agent, decision=decision,
        reasoning="Gate B at 94% capacity.",
        confidence=confidence, outcome=outcome,
        affected_fans=1400, impact_pct=23.0,
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return d


def make_event(
    db: Session,
    title: str = "Gate B congestion",
    event_type: str = "crowd",
    severity: int = 3
) -> StadiumEvent:
    """
    Create a test StadiumEvent in the database.
    """
    e = StadiumEvent(
        event_type=event_type, title=title,
        description="AI-detected crowd pressure",
        severity=severity, zone="Gate B", resolved=False,
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return e
