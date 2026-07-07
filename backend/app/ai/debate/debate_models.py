"""
StadiumVerse AI V2 - Debate Models
Data structures for AI agent debate and decision making
"""

import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class AgentRole(str, Enum):
    """Roles for AI agents in the debate system"""

    COORDINATOR = "coordinator"
    NAVIGATION = "navigation"
    SECURITY = "security"
    MEDICAL = "medical"
    VOLUNTEER = "volunteer"
    FOOD = "food"
    TRANSPORT = "transport"
    ACCESSIBILITY = "accessibility"
    WEATHER = "weather"
    SUSTAINABILITY = "sustainability"
    EMERGENCY = "emergency"
    CLEANING = "cleaning"
    ANALYTICS = "analytics"


class DebateStatus(str, Enum):
    """Status of debate sessions"""

    INITIATED = "initiated"
    GATHERING_POSITIONS = "gathering_positions"
    ANALYZING = "analyzing"
    CONCLUDED = "concluded"
    OVERRIDDEN = "overridden"
    FAILED = "failed"


@dataclass
class AgentPosition:
    """Position taken by an AI agent in a debate"""

    agent_name: AgentRole
    recommendation: str
    reasoning: str
    confidence: float  # 0.0 to 1.0
    risk_assessment: str  # low, medium, high, critical
    alternative_actions: List[str] = field(default_factory=list)
    estimated_cost: float = 0.0
    estimated_impact: str = ""
    supporting_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def get_position_strength(self) -> float:
        """Calculate overall strength of this position"""
        # Base on confidence and risk assessment
        risk_penalties = {"low": 0.0, "medium": 0.1, "high": 0.2, "critical": 0.4}

        risk_penalty = risk_penalties.get(self.risk_assessment.lower(), 0.1)
        strength = self.confidence - risk_penalty

        # Bonus for having alternatives and supporting data
        if self.alternative_actions:
            strength += 0.05
        if self.supporting_data:
            strength += 0.05

        return max(0.0, min(1.0, strength))

    def to_dict(self) -> Dict[str, Any]:
        """Convert position to dictionary"""
        return {
            "agent_name": self.agent_name.value,
            "recommendation": self.recommendation,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "risk_assessment": self.risk_assessment,
            "alternative_actions": self.alternative_actions,
            "estimated_cost": self.estimated_cost,
            "estimated_impact": self.estimated_impact,
            "supporting_data": self.supporting_data,
            "position_strength": self.get_position_strength(),
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class DebateDecision:
    """Final decision reached through AI debate"""

    decision: str
    reasoning: str
    confidence: float  # 0.0 to 1.0
    risk_level: str  # low, medium, high, critical
    implementation_steps: List[str] = field(default_factory=list)
    estimated_timeline: str = ""
    success_probability: float = 0.5
    fallback_plan: str = ""
    affected_fans: int = 0
    resource_requirements: List[str] = field(default_factory=list)
    roi_analysis: Dict[str, Any] = field(default_factory=dict)
    carbon_impact: float = 0.0
    consensus_score: float = 0.0
    dissenting_agents: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def get_decision_quality_score(self) -> float:
        """Calculate overall quality score for this decision"""
        # Components of decision quality
        confidence_component = self.confidence * 0.3
        consensus_component = self.consensus_score * 0.25
        success_component = self.success_probability * 0.2

        # Risk penalty
        risk_penalties = {"low": 0.0, "medium": 0.05, "high": 0.1, "critical": 0.2}
        risk_penalty = risk_penalties.get(self.risk_level.lower(), 0.05)

        # Implementation quality bonus
        implementation_bonus = 0.0
        if self.implementation_steps and len(self.implementation_steps) >= 3:
            implementation_bonus += 0.1
        if self.fallback_plan:
            implementation_bonus += 0.05
        if self.resource_requirements:
            implementation_bonus += 0.05

        quality = (
            confidence_component
            + consensus_component
            + success_component
            + implementation_bonus
            - risk_penalty
        )

        return max(0.0, min(1.0, quality))

    def to_dict(self) -> Dict[str, Any]:
        """Convert decision to dictionary"""
        return {
            "decision": self.decision,
            "reasoning": self.reasoning,
            "confidence": self.confidence,
            "risk_level": self.risk_level,
            "implementation_steps": self.implementation_steps,
            "estimated_timeline": self.estimated_timeline,
            "success_probability": self.success_probability,
            "fallback_plan": self.fallback_plan,
            "affected_fans": self.affected_fans,
            "resource_requirements": self.resource_requirements,
            "roi_analysis": self.roi_analysis,
            "carbon_impact": self.carbon_impact,
            "consensus_score": self.consensus_score,
            "dissenting_agents": self.dissenting_agents,
            "decision_quality_score": self.get_decision_quality_score(),
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class DebateSession:
    """Complete AI debate session with all positions and final decision"""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    topic: str = ""
    context: Dict[str, Any] = field(default_factory=dict)
    trigger_event: str = ""
    urgency_level: int = 3  # 1-5 scale

    agent_positions: List[AgentPosition] = field(default_factory=list)
    final_decision: Optional[DebateDecision] = None
    status: DebateStatus = DebateStatus.INITIATED

    started_at: datetime = field(default_factory=datetime.utcnow)
    concluded_at: Optional[datetime] = None
    total_duration_seconds: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_agent_position(self, position: AgentPosition):
        """Add an agent position to the debate"""
        self.agent_positions.append(position)

    def conclude_debate(self, decision: DebateDecision):
        """Conclude the debate with final decision"""
        self.final_decision = decision
        self.status = DebateStatus.CONCLUDED
        self.concluded_at = datetime.utcnow()
        self.total_duration_seconds = (
            self.concluded_at - self.started_at
        ).total_seconds()

        # Calculate consensus score
        consensus_score = self.get_consensus_score()
        self.final_decision.consensus_score = consensus_score

        # Identify dissenting agents
        dissenting_agents = self.get_dissenting_agents()
        self.final_decision.dissenting_agents = dissenting_agents

    def get_consensus_score(self) -> float:
        """Calculate consensus score across all agent positions"""
        if not self.agent_positions:
            return 0.0

        # Get all recommendations
        recommendations = [pos.recommendation.lower() for pos in self.agent_positions]

        # Simple consensus: what percentage of agents agree with most common recommendation?
        if not recommendations:
            return 0.0

        # Find most common recommendation
        from collections import Counter

        recommendation_counts = Counter(recommendations)
        most_common_rec, most_common_count = recommendation_counts.most_common(1)[0]

        # Calculate consensus as percentage agreement
        consensus_ratio = most_common_count / len(recommendations)

        # Weight by average confidence of agreeing agents
        agreeing_agents = [
            pos
            for pos in self.agent_positions
            if pos.recommendation.lower() == most_common_rec
        ]
        avg_confidence = sum(pos.confidence for pos in agreeing_agents) / len(
            agreeing_agents
        )

        # Combine consensus ratio and confidence
        consensus_score = (consensus_ratio * 0.7) + (avg_confidence * 0.3)

        return min(1.0, max(0.0, consensus_score))

    def get_dissenting_agents(self) -> List[str]:
        """Get list of agents that dissent from the majority"""
        if not self.agent_positions or not self.final_decision:
            return []

        # Find most common recommendation
        recommendations = [pos.recommendation.lower() for pos in self.agent_positions]
        from collections import Counter

        most_common_rec = Counter(recommendations).most_common(1)[0][0]

        # Find agents that disagree
        dissenting_agents = []
        for pos in self.agent_positions:
            if pos.recommendation.lower() != most_common_rec:
                dissenting_agents.append(pos.agent_name.value)

        return dissenting_agents

    def get_risk_distribution(self) -> Dict[str, int]:
        """Get distribution of risk assessments across agents"""
        risk_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}

        for position in self.agent_positions:
            risk_level = position.risk_assessment.lower()
            if risk_level in risk_counts:
                risk_counts[risk_level] += 1

        return risk_counts

    def get_average_confidence(self) -> float:
        """Get average confidence across all agent positions"""
        if not self.agent_positions:
            return 0.0

        total_confidence = sum(pos.confidence for pos in self.agent_positions)
        return total_confidence / len(self.agent_positions)

    def get_cost_estimates(self) -> Dict[str, float]:
        """Get cost estimate statistics"""
        if not self.agent_positions:
            return {"min": 0.0, "max": 0.0, "average": 0.0}

        costs = [
            pos.estimated_cost for pos in self.agent_positions if pos.estimated_cost > 0
        ]

        if not costs:
            return {"min": 0.0, "max": 0.0, "average": 0.0}

        return {
            "min": min(costs),
            "max": max(costs),
            "average": sum(costs) / len(costs),
        }

    def get_debate_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of the debate"""
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "trigger_event": self.trigger_event,
            "urgency_level": self.urgency_level,
            "status": self.status.value,
            "participants": len(self.agent_positions),
            "duration_seconds": self.total_duration_seconds,
            "consensus_score": self.get_consensus_score(),
            "average_confidence": self.get_average_confidence(),
            "risk_distribution": self.get_risk_distribution(),
            "cost_estimates": self.get_cost_estimates(),
            "final_decision": self.final_decision.to_dict()
            if self.final_decision
            else None,
            "agent_positions": [pos.to_dict() for pos in self.agent_positions],
            "started_at": self.started_at.isoformat(),
            "concluded_at": self.concluded_at.isoformat()
            if self.concluded_at
            else None,
        }

    def get_position_by_agent(self, agent_role: AgentRole) -> Optional[AgentPosition]:
        """Get position from specific agent"""
        for position in self.agent_positions:
            if position.agent_name == agent_role:
                return position
        return None

    def get_high_confidence_positions(
        self, min_confidence: float = 0.8
    ) -> List[AgentPosition]:
        """Get positions with confidence above threshold"""
        return [pos for pos in self.agent_positions if pos.confidence >= min_confidence]

    def get_high_risk_positions(self) -> List[AgentPosition]:
        """Get positions that identify high or critical risk"""
        return [
            pos
            for pos in self.agent_positions
            if pos.risk_assessment.lower() in ["high", "critical"]
        ]

    def to_dict(self) -> Dict[str, Any]:
        """Convert debate session to dictionary"""
        return self.get_debate_summary()


@dataclass
class DebateAnalytics:
    """Analytics for debate system performance"""

    total_debates: int = 0
    successful_decisions: int = 0
    average_consensus_score: float = 0.0
    average_decision_quality: float = 0.0
    average_duration_seconds: float = 0.0
    most_active_agents: List[str] = field(default_factory=list)
    common_topics: List[str] = field(default_factory=list)
    risk_level_distribution: Dict[str, int] = field(default_factory=dict)
    agent_agreement_matrix: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def update_analytics(self, debate_session: DebateSession):
        """Update analytics with new debate session"""
        self.total_debates += 1

        if debate_session.final_decision:
            self.successful_decisions += 1

            # Update running averages
            new_consensus = debate_session.get_consensus_score()
            new_quality = debate_session.final_decision.get_decision_quality_score()
            new_duration = debate_session.total_duration_seconds

            # Calculate new running averages
            self.average_consensus_score = (
                self.average_consensus_score * (self.successful_decisions - 1)
                + new_consensus
            ) / self.successful_decisions

            self.average_decision_quality = (
                self.average_decision_quality * (self.successful_decisions - 1)
                + new_quality
            ) / self.successful_decisions

            self.average_duration_seconds = (
                self.average_duration_seconds * (self.total_debates - 1) + new_duration
            ) / self.total_debates

            # Update risk distribution
            risk_level = debate_session.final_decision.risk_level
            if risk_level not in self.risk_level_distribution:
                self.risk_level_distribution[risk_level] = 0
            self.risk_level_distribution[risk_level] += 1

    def get_success_rate(self) -> float:
        """Get overall debate success rate"""
        if self.total_debates == 0:
            return 0.0
        return self.successful_decisions / self.total_debates

    def to_dict(self) -> Dict[str, Any]:
        """Convert analytics to dictionary"""
        return {
            "total_debates": self.total_debates,
            "successful_decisions": self.successful_decisions,
            "success_rate": self.get_success_rate(),
            "average_consensus_score": self.average_consensus_score,
            "average_decision_quality": self.average_decision_quality,
            "average_duration_seconds": self.average_duration_seconds,
            "most_active_agents": self.most_active_agents,
            "common_topics": self.common_topics,
            "risk_level_distribution": self.risk_level_distribution,
            "agent_agreement_matrix": self.agent_agreement_matrix,
        }
