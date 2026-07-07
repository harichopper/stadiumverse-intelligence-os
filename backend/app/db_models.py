"""
StadiumVerse Intelligence OS — SQLite Models
All tables in one file, SQLite-compatible (no PostGIS / UUID columns).
"""

import uuid
from datetime import datetime
from typing import Any, Dict
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .database import Base


def _uid() -> str:
    """Generate a unique UUID string for primary keys."""
    return str(uuid.uuid4())


# ── Fans ──────────────────────────────────────────────────────────────────────
class DigitalFan(Base):
    """
    Digital twin of a stadium fan, tracking personal details, live state,
    and AI predictions for behavior and risk.
    """

    __tablename__ = "digital_fans"

    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(3), nullable=False)
    flag = Column(String(10), default="🏳️")
    language = Column(String(10), default="en")
    age = Column(Integer, default=30)
    favorite_team = Column(String(100))
    sector = Column(String(20), default="A")
    seat = Column(String(20))

    # Live emotional and physical state
    current_emotion = Column(String(30), default="neutral")
    stress_level = Column(Integer, default=50)
    excitement_level = Column(Integer, default=50)
    hunger_level = Column(Integer, default=30)
    fatigue_level = Column(Integer, default=20)

    # Location (normalized X/Y: 0-100)
    loc_x = Column(Float, default=50.0)
    loc_y = Column(Float, default=50.0)

    # AI-generated fields
    current_thought = Column(Text)
    memory_summary = Column(Text)
    predicted_action = Column(Text)
    prediction_confidence = Column(Float, default=0.5)
    risk_score = Column(Integer, default=20)

    # Meta fields
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    movements = relationship(
        "FanMovement", back_populates="fan", cascade="all, delete-orphan"
    )
    predictions = relationship(
        "FanPrediction", back_populates="fan", cascade="all, delete-orphan"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serializable dictionary for API responses."""
        return {
            "id": self.id,
            "fan_id": self.fan_id,
            "name": self.name,
            "country": self.country,
            "flag": self.flag,
            "language": self.language,
            "age": self.age,
            "favorite_team": self.favorite_team,
            "sector": self.sector,
            "seat": self.seat,
            "current_emotion": self.current_emotion,
            "stress_level": self.stress_level,
            "excitement_level": self.excitement_level,
            "hunger_level": self.hunger_level,
            "fatigue_level": self.fatigue_level,
            "loc_x": self.loc_x,
            "loc_y": self.loc_y,
            "current_thought": self.current_thought,
            "memory_summary": self.memory_summary,
            "predicted_action": self.predicted_action,
            "prediction_confidence": self.prediction_confidence,
            "risk_score": self.risk_score,
            "is_active": self.is_active,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class FanMovement(Base):
    """
    Historical movement record for a digital fan twin.
    """

    __tablename__ = "fan_movements"

    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(String(36), ForeignKey("digital_fans.id"), nullable=False)
    loc_x = Column(Float, nullable=False)
    loc_y = Column(Float, nullable=False)
    speed = Column(Float, default=1.2)
    timestamp = Column(DateTime, default=datetime.utcnow)

    fan = relationship("DigitalFan", back_populates="movements")


class FanPrediction(Base):
    """
    AI-generated prediction for a digital fan's future behavior.
    """

    __tablename__ = "fan_predictions"

    id = Column(String(36), primary_key=True, default=_uid)
    fan_id = Column(String(36), ForeignKey("digital_fans.id"), nullable=False)
    prediction_type = Column(String(30), nullable=False)
    description = Column(Text)
    confidence_score = Column(Float, default=0.5)
    predicted_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fan = relationship("DigitalFan", back_populates="predictions")


# ── Volunteers ────────────────────────────────────────────────────────────────
class Volunteer(Base):
    """
    Stadium volunteer profile, tracking skills, availability, and assignments.
    """

    __tablename__ = "volunteers"

    id = Column(String(36), primary_key=True, default=_uid)
    volunteer_id = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    languages = Column(String(200), default="en")  # Comma-separated
    skills = Column(String(200), default="general")  # Comma-separated
    medical_training = Column(Boolean, default=False)
    availability = Column(String(20), default="available")
    zone_assignment = Column(String(50))
    loc_x = Column(Float, default=50.0)
    loc_y = Column(Float, default=50.0)
    tasks_today = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tasks = relationship(
        "VolunteerTask", back_populates="volunteer", cascade="all, delete-orphan"
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serializable dictionary for API responses."""
        return {
            "id": self.id,
            "volunteer_id": self.volunteer_id,
            "name": self.name,
            "languages": self.languages.split(",") if self.languages else [],
            "skills": self.skills.split(",") if self.skills else [],
            "medical_training": self.medical_training,
            "availability": self.availability,
            "zone_assignment": self.zone_assignment,
            "loc_x": self.loc_x,
            "loc_y": self.loc_y,
            "tasks_today": self.tasks_today,
            "is_active": self.is_active,
        }


class VolunteerTask(Base):
    """
    Task assigned to a volunteer (manual or AI-generated).
    """

    __tablename__ = "volunteer_tasks"

    id = Column(String(36), primary_key=True, default=_uid)
    volunteer_id = Column(String(36), ForeignKey("volunteers.id"), nullable=False)
    task_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=3)  # 1=low, 5=high
    status = Column(String(20), default="assigned")
    assigned_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    assigned_by_ai = Column(Boolean, default=False)

    volunteer = relationship("Volunteer", back_populates="tasks")

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serializable dictionary for API responses."""
        return {
            "id": self.id,
            "volunteer_id": self.volunteer_id,
            "task_type": self.task_type,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "assigned_by_ai": self.assigned_by_ai,
        }


# ── Crowd Analytics ───────────────────────────────────────────────────────────
class CrowdSnapshot(Base):
    """
    Point-in-time snapshot of overall crowd state and analytics.
    """

    __tablename__ = "crowd_snapshots"

    id = Column(String(36), primary_key=True, default=_uid)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    total_fans = Column(Integer, default=0)
    avg_stress = Column(Float, default=50.0)
    avg_excitement = Column(Float, default=50.0)
    risk_level = Column(String(20), default="healthy")  # healthy/warning/critical
    gate_a_density = Column(Float, default=0.0)
    gate_b_density = Column(Float, default=0.0)
    gate_c_density = Column(Float, default=0.0)
    gate_d_density = Column(Float, default=0.0)
    queue_avg_min = Column(Float, default=5.0)
    weather_temp = Column(Float, default=22.0)
    weather_rain_pct = Column(Float, default=0.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serializable dictionary for API responses."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "total_fans": self.total_fans,
            "avg_stress": self.avg_stress,
            "avg_excitement": self.avg_excitement,
            "risk_level": self.risk_level,
            "gate_densities": {
                "A": self.gate_a_density,
                "B": self.gate_b_density,
                "C": self.gate_c_density,
                "D": self.gate_d_density,
            },
            "queue_avg_min": self.queue_avg_min,
            "weather": {"temp": self.weather_temp, "rain_pct": self.weather_rain_pct},
        }


# ── AI Decisions (Black Box Recorder) ────────────────────────────────────────
class AIDecision(Base):
    """
    Record of all AI decisions made, with reasoning, confidence, and outcomes.
    """

    __tablename__ = "ai_decisions"

    id = Column(String(36), primary_key=True, default=_uid)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    match_minute = Column(Integer, default=0)
    agent = Column(String(50), default="Coordinator")
    decision = Column(Text, nullable=False)
    reasoning = Column(Text)
    confidence = Column(Float, default=0.85)
    outcome = Column(String(20), default="PENDING")  # SUCCESS/PARTIAL/FAILED/PENDING
    affected_fans = Column(Integer, default=0)
    impact_pct = Column(Float, default=0.0)  # % improvement

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serializable dictionary for API responses."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "match_minute": self.match_minute,
            "agent": self.agent,
            "decision": self.decision,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "outcome": self.outcome,
            "affected_fans": self.affected_fans,
            "impact_pct": self.impact_pct,
        }


# ── Stadium Events ────────────────────────────────────────────────────────────
class StadiumEvent(Base):
    """
    Record of significant events happening in or around the stadium.
    """

    __tablename__ = "stadium_events"

    id = Column(String(36), primary_key=True, default=_uid)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    event_type = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    severity = Column(Integer, default=2)  # 1-5 (1=low, 5=critical)
    zone = Column(String(50))
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to a serializable dictionary for API responses."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "event_type": self.event_type,
            "title": self.title,
            "description": self.description,
            "severity": self.severity,
            "zone": self.zone,
            "resolved": self.resolved,
        }
