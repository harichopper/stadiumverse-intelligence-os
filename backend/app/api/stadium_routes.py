"""
StadiumVerse Intelligence OS — Stadium API Routes
All REST endpoints consumed by the frontend.
"""

import random
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from ..database import get_db
from ..db_models import (
    DigitalFan,
    Volunteer,
    VolunteerTask,
    CrowdSnapshot,
    AIDecision,
    StadiumEvent,
)

router = APIRouter(prefix="/api/stadium", tags=["stadium"])


# ── Fans ──────────────────────────────────────────────────────────────────────
@router.get("/fans")
def list_fans(
    active_only: bool = True,
    limit: int = Query(default=50, le=200),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve a list of digital fan twins."""
    q = db.query(DigitalFan)
    if active_only:
        q = q.filter(DigitalFan.is_active)
    fans = q.limit(limit).all()
    return {"fans": [f.to_dict() for f in fans], "total": q.count()}


@router.get("/fans/{fan_id}")
def get_fan(fan_id: str, db: Session = Depends(get_db)) -> dict:
    """Retrieve details for a specific fan twin."""
    fan = (
        db.query(DigitalFan)
        .filter((DigitalFan.id == fan_id) | (DigitalFan.fan_id == fan_id))
        .first()
    )
    if not fan:
        raise HTTPException(status_code=404, detail="Fan not found")
    return fan.to_dict()


@router.patch("/fans/{fan_id}/stress")
def update_fan_stress(fan_id: str, stress: int, db: Session = Depends(get_db)) -> dict:
    """Update the stress level of a specific fan twin."""
    fan = db.query(DigitalFan).filter(DigitalFan.fan_id == fan_id).first()
    if not fan:
        raise HTTPException(status_code=404, detail="Fan not found")
    fan.stress_level = max(0, min(100, stress))
    db.commit()
    return {"updated": True, "stress_level": fan.stress_level}


# ── Volunteers ────────────────────────────────────────────────────────────────
@router.get("/volunteers")
def list_volunteers(
    available_only: bool = False,
    db: Session = Depends(get_db),
) -> dict:
    """List all stadium volunteers."""
    q = db.query(Volunteer).filter(Volunteer.is_active)
    if available_only:
        q = q.filter(Volunteer.availability == "available")
    vols = q.all()
    return {"volunteers": [v.to_dict() for v in vols], "total": len(vols)}


@router.post("/volunteers/{volunteer_id}/deploy")
def deploy_volunteer(volunteer_id: str, zone: str, db: Session = Depends(get_db)):
    vol = db.query(Volunteer).filter(Volunteer.volunteer_id == volunteer_id).first()
    if not vol:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    vol.availability = "busy"
    vol.zone_assignment = zone
    task = VolunteerTask(
        volunteer_id=vol.id,
        task_type="crowd_control",
        title=f"Deployed to {zone}",
        description="AI-triggered deployment",
        priority=4,
        status="in_progress",
        assigned_by_ai=True,
    )
    db.add(task)
    db.commit()
    return {"deployed": True, "volunteer": vol.to_dict()}


# ── Crowd analytics ───────────────────────────────────────────────────────────
@router.get("/crowd/current")
def current_crowd(db: Session = Depends(get_db)) -> dict:
    """Get the most recent crowd snapshot."""
    snap = db.query(CrowdSnapshot).order_by(desc(CrowdSnapshot.timestamp)).first()
    if not snap:
        return {"message": "No snapshot yet"}
    return snap.to_dict()


@router.get("/crowd/history")
def crowd_history(
    minutes: int = Query(default=90, le=180),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve historical crowd snapshots."""
    since = datetime.utcnow() - timedelta(minutes=minutes)
    snaps = (
        db.query(CrowdSnapshot)
        .filter(CrowdSnapshot.timestamp >= since)
        .order_by(CrowdSnapshot.timestamp)
        .all()
    )
    return {"snapshots": [s.to_dict() for s in snaps]}


@router.post("/crowd/snapshot")
def create_snapshot(db: Session = Depends(get_db)):
    """Simulate a live crowd snapshot (called periodically by frontend or scheduler)."""
    last = db.query(CrowdSnapshot).order_by(desc(CrowdSnapshot.timestamp)).first()
    base_fans = last.total_fans if last else 87342

    snap = CrowdSnapshot(
        total_fans=base_fans + random.randint(-200, 200),
        avg_stress=last.avg_stress + random.uniform(-2, 2) if last else 50,
        avg_excitement=last.avg_excitement + random.uniform(-2, 2) if last else 60,
        risk_level=last.risk_level if last else "healthy",
        gate_a_density=min(
            99, (last.gate_a_density if last else 65) + random.uniform(-3, 3)
        ),
        gate_b_density=min(
            99, (last.gate_b_density if last else 87) + random.uniform(-2, 4)
        ),
        gate_c_density=min(
            99, (last.gate_c_density if last else 70) + random.uniform(-3, 3)
        ),
        gate_d_density=min(
            99, (last.gate_d_density if last else 60) + random.uniform(-3, 3)
        ),
        queue_avg_min=(last.queue_avg_min if last else 5) + random.uniform(-0.5, 0.5),
        weather_temp=(last.weather_temp if last else 22) + random.uniform(-0.1, 0.1),
        weather_rain_pct=min(
            100, max(0, (last.weather_rain_pct if last else 18) + random.uniform(-1, 1))
        ),
    )
    db.add(snap)
    db.commit()
    return snap.to_dict()


# ── AI Decisions ──────────────────────────────────────────────────────────────
@router.get("/decisions")
def list_decisions(
    limit: int = Query(default=20, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """List recent AI decisions."""
    decisions = (
        db.query(AIDecision).order_by(desc(AIDecision.timestamp)).limit(limit).all()
    )
    return {"decisions": [d.to_dict() for d in decisions]}


@router.post("/decisions")
def record_decision(
    agent: str,
    decision: str,
    reasoning: str = "",
    confidence: float = 0.85,
    match_minute: int = 67,
    affected_fans: int = 0,
    db: Session = Depends(get_db),
):
    d = AIDecision(
        match_minute=match_minute,
        agent=agent,
        decision=decision,
        reasoning=reasoning,
        confidence=confidence,
        outcome="PENDING",
        affected_fans=affected_fans,
    )
    db.add(d)
    db.commit()
    return d.to_dict()


@router.patch("/decisions/{decision_id}/outcome")
def update_outcome(
    decision_id: str,
    outcome: str,
    impact_pct: float = 0.0,
    db: Session = Depends(get_db),
):
    d = db.query(AIDecision).filter(AIDecision.id == decision_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Decision not found")
    d.outcome = outcome
    d.impact_pct = impact_pct
    db.commit()
    return d.to_dict()


# ── Stadium Events ────────────────────────────────────────────────────────────
@router.get("/events")
def list_events(
    limit: int = Query(default=30, le=100),
    db: Session = Depends(get_db),
) -> dict:
    """List recent stadium events."""
    events = (
        db.query(StadiumEvent).order_by(desc(StadiumEvent.timestamp)).limit(limit).all()
    )
    return {"events": [e.to_dict() for e in events]}


# ── Dashboard summary ─────────────────────────────────────────────────────────
@router.get("/dashboard")
def dashboard_summary(db: Session = Depends(get_db)):
    """Single endpoint the frontend polls for the full dashboard state."""
    snap = db.query(CrowdSnapshot).order_by(desc(CrowdSnapshot.timestamp)).first()
    fan_count = db.query(DigitalFan).filter(DigitalFan.is_active).count()
    vol_available = (
        db.query(Volunteer)
        .filter(Volunteer.availability == "available", Volunteer.is_active)
        .count()
    )
    recent_decisions = (
        db.query(AIDecision).order_by(desc(AIDecision.timestamp)).limit(5).all()
    )
    recent_events = (
        db.query(StadiumEvent).order_by(desc(StadiumEvent.timestamp)).limit(5).all()
    )

    return {
        "crowd": snap.to_dict() if snap else {},
        "fans_online": fan_count,
        "volunteers_available": vol_available,
        "recent_decisions": [d.to_dict() for d in recent_decisions],
        "recent_events": [e.to_dict() for e in recent_events],
        "timestamp": datetime.utcnow().isoformat(),
    }
