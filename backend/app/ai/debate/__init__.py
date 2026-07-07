"""
StadiumVerse AI V2 - AI Debate System
Multi-agent debate and reasoning system for critical decisions
"""

from .debate_chamber import DebateChamber
from .debate_coordinator import DebateCoordinator
from .debate_models import AgentPosition, DebateDecision, DebateSession

__all__ = [
    "DebateCoordinator",
    "DebateSession",
    "AgentPosition",
    "DebateDecision",
    "DebateChamber",
]
