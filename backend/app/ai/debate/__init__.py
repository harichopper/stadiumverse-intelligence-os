"""
StadiumVerse AI V2 - AI Debate System
Multi-agent debate and reasoning system for critical decisions
"""

from .debate_coordinator import DebateCoordinator
from .debate_models import DebateSession, AgentPosition, DebateDecision
from .debate_chamber import DebateChamber

__all__ = [
    "DebateCoordinator",
    "DebateSession", 
    "AgentPosition",
    "DebateDecision",
    "DebateChamber"
]