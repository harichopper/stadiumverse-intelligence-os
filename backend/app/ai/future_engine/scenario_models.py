"""
StadiumVerse AI V2 - Future Scenario Models
Data structures for multi-branch future predictions
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional


class BranchType(str, Enum):
    BEST_CASE = "best_case"
    MOST_LIKELY = "most_likely"
    WORST_CASE = "worst_case"


class OutcomeCategory(str, Enum):
    CROWD_DENSITY = "crowd_density"
    QUEUE_TIMES = "queue_times"
    FAN_SATISFACTION = "fan_satisfaction"
    MEDICAL_INCIDENTS = "medical_incidents"
    REVENUE_IMPACT = "revenue_impact"
    CARBON_FOOTPRINT = "carbon_footprint"
    VOLUNTEER_LOAD = "volunteer_load"
    TRANSPORT_EFFICIENCY = "transport_efficiency"


@dataclass
class TimelinePoint:
    """A specific point in time with predicted conditions"""

    timestamp: datetime
    minutes_from_now: int
    crowd_density: float  # 0.0 to 1.0
    avg_queue_time: float  # minutes
    fan_satisfaction: float  # 0.0 to 100.0
    medical_risk_level: float  # 0.0 to 1.0
    revenue_rate: float  # $/minute
    carbon_output: float  # kg CO2/hour
    volunteer_utilization: float  # 0.0 to 1.0
    transport_efficiency: float  # 0.0 to 1.0
    key_events: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "minutes_from_now": self.minutes_from_now,
            "crowd_density": self.crowd_density,
            "avg_queue_time": self.avg_queue_time,
            "fan_satisfaction": self.fan_satisfaction,
            "medical_risk_level": self.medical_risk_level,
            "revenue_rate": self.revenue_rate,
            "carbon_output": self.carbon_output,
            "volunteer_utilization": self.volunteer_utilization,
            "transport_efficiency": self.transport_efficiency,
            "key_events": self.key_events,
        }


@dataclass
class ScenarioOutcome:
    """Outcome metrics for a specific scenario branch"""

    category: OutcomeCategory
    current_value: float
    predicted_value: float
    change_percentage: float
    confidence: float  # 0.0 to 1.0
    impact_description: str
    contributing_factors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "current_value": self.current_value,
            "predicted_value": self.predicted_value,
            "change_percentage": self.change_percentage,
            "confidence": self.confidence,
            "impact_description": self.impact_description,
            "contributing_factors": self.contributing_factors,
        }


@dataclass
class FutureBranch:
    """A complete future scenario branch with timeline and outcomes"""

    branch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    branch_type: BranchType = BranchType.MOST_LIKELY
    title: str = ""
    description: str = ""
    probability: float = 0.33  # 0.0 to 1.0

    # Timeline predictions
    timeline_points: List[TimelinePoint] = field(default_factory=list)

    # Outcome categories
    outcomes: Dict[OutcomeCategory, ScenarioOutcome] = field(default_factory=dict)

    # Overall metrics
    overall_risk_score: float = 0.5  # 0.0 to 1.0
    overall_satisfaction_score: float = 70.0  # 0.0 to 100.0
    resource_efficiency_score: float = 0.7  # 0.0 to 1.0

    # Key differentiators
    critical_decisions: List[str] = field(default_factory=list)
    intervention_opportunities: List[str] = field(default_factory=list)
    risk_mitigation_strategies: List[str] = field(default_factory=list)

    # Metadata
    generated_at: datetime = field(default_factory=datetime.utcnow)
    valid_until: datetime = field(
        default_factory=lambda: datetime.utcnow() + timedelta(hours=2)
    )
    confidence_score: float = 0.7
    data_sources: List[str] = field(default_factory=list)

    def add_timeline_point(self, point: TimelinePoint):
        """Add a timeline point and sort by timestamp"""
        self.timeline_points.append(point)
        self.timeline_points.sort(key=lambda p: p.timestamp)

    def add_outcome(self, outcome: ScenarioOutcome):
        """Add an outcome for a specific category"""
        self.outcomes[outcome.category] = outcome

    def get_timeline_at_minutes(self, minutes: int) -> Optional[TimelinePoint]:
        """Get timeline point closest to specified minutes from now"""
        closest_point = None
        min_diff = float("inf")

        for point in self.timeline_points:
            diff = abs(point.minutes_from_now - minutes)
            if diff < min_diff:
                min_diff = diff
                closest_point = point

        return closest_point

    def get_peak_risk_time(self) -> Optional[TimelinePoint]:
        """Find the timeline point with highest risk"""
        if not self.timeline_points:
            return None

        return max(
            self.timeline_points, key=lambda p: p.medical_risk_level + p.crowd_density
        )

    def get_bottleneck_predictions(self) -> List[Dict[str, Any]]:
        """Identify predicted bottlenecks and their timing"""
        bottlenecks = []

        for point in self.timeline_points:
            # High crowd density bottleneck
            if point.crowd_density > 0.8:
                bottlenecks.append(
                    {
                        "type": "crowd_congestion",
                        "time": point.timestamp.isoformat(),
                        "severity": point.crowd_density,
                        "description": f"Crowd density reaches {point.crowd_density:.0%} at {point.timestamp.strftime('%H:%M')}",
                    }
                )

            # Long queue bottleneck
            if point.avg_queue_time > 15:
                bottlenecks.append(
                    {
                        "type": "queue_delays",
                        "time": point.timestamp.isoformat(),
                        "severity": point.avg_queue_time,
                        "description": f"Average queue time exceeds {point.avg_queue_time:.0f} minutes",
                    }
                )

            # Volunteer overload
            if point.volunteer_utilization > 0.9:
                bottlenecks.append(
                    {
                        "type": "volunteer_overload",
                        "time": point.timestamp.isoformat(),
                        "severity": point.volunteer_utilization,
                        "description": f"Volunteer utilization reaches {point.volunteer_utilization:.0%}",
                    }
                )

        return sorted(bottlenecks, key=lambda b: b["severity"], reverse=True)[:5]

    def calculate_intervention_score(self) -> float:
        """Calculate how much this branch could benefit from intervention"""
        risk_factors = [
            self.overall_risk_score,
            max([p.medical_risk_level for p in self.timeline_points] or [0]),
            max([p.crowd_density for p in self.timeline_points] or [0]),
            1.0 - (self.overall_satisfaction_score / 100.0),
        ]

        base_intervention_score = sum(risk_factors) / len(risk_factors)

        # Boost score if there are clear intervention opportunities
        opportunity_boost = len(self.intervention_opportunities) * 0.1

        return min(1.0, base_intervention_score + opportunity_boost)

    def to_dict(self) -> Dict[str, Any]:
        """Convert branch to dictionary for API responses"""
        return {
            "branch_id": self.branch_id,
            "branch_type": self.branch_type.value,
            "title": self.title,
            "description": self.description,
            "probability": self.probability,
            # Timeline
            "timeline_points": [point.to_dict() for point in self.timeline_points],
            "timeline_summary": {
                "total_points": len(self.timeline_points),
                "peak_risk_time": self.get_peak_risk_time().timestamp.isoformat()
                if self.get_peak_risk_time()
                else None,
                "bottlenecks": self.get_bottleneck_predictions(),
            },
            # Outcomes
            "outcomes": {
                cat.value: outcome.to_dict() for cat, outcome in self.outcomes.items()
            },
            # Overall scores
            "overall_risk_score": self.overall_risk_score,
            "overall_satisfaction_score": self.overall_satisfaction_score,
            "resource_efficiency_score": self.resource_efficiency_score,
            "intervention_score": self.calculate_intervention_score(),
            # Strategic elements
            "critical_decisions": self.critical_decisions,
            "intervention_opportunities": self.intervention_opportunities,
            "risk_mitigation_strategies": self.risk_mitigation_strategies,
            # Metadata
            "generated_at": self.generated_at.isoformat(),
            "valid_until": self.valid_until.isoformat(),
            "confidence_score": self.confidence_score,
            "data_sources": self.data_sources,
        }


@dataclass
class FutureBranchSet:
    """A complete set of future branches (best/likely/worst) for comparison"""

    prediction_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_name: str = ""
    trigger_context: Dict[str, Any] = field(default_factory=dict)

    best_case: Optional[FutureBranch] = None
    most_likely: Optional[FutureBranch] = None
    worst_case: Optional[FutureBranch] = None

    # Comparative analysis
    variance_analysis: Dict[str, Any] = field(default_factory=dict)
    decision_impact_analysis: Dict[str, Any] = field(default_factory=dict)

    generated_at: datetime = field(default_factory=datetime.utcnow)

    def add_branch(self, branch: FutureBranch):
        """Add a branch to the appropriate slot"""
        if branch.branch_type == BranchType.BEST_CASE:
            self.best_case = branch
        elif branch.branch_type == BranchType.MOST_LIKELY:
            self.most_likely = branch
        elif branch.branch_type == BranchType.WORST_CASE:
            self.worst_case = branch

    def calculate_variance_analysis(self):
        """Calculate variance between branches"""
        branches = [b for b in [self.best_case, self.most_likely, self.worst_case] if b]

        if len(branches) < 2:
            return

        # Risk variance
        risk_scores = [b.overall_risk_score for b in branches]
        risk_variance = max(risk_scores) - min(risk_scores)

        # Satisfaction variance
        satisfaction_scores = [b.overall_satisfaction_score for b in branches]
        satisfaction_variance = max(satisfaction_scores) - min(satisfaction_scores)

        # Timeline variance (peak crowd density difference)
        peak_densities = []
        for branch in branches:
            peak = max([p.crowd_density for p in branch.timeline_points] or [0])
            peak_densities.append(peak)
        density_variance = max(peak_densities) - min(peak_densities)

        self.variance_analysis = {
            "risk_variance": risk_variance,
            "satisfaction_variance": satisfaction_variance,
            "crowd_density_variance": density_variance,
            "high_variance": risk_variance > 0.3
            or satisfaction_variance > 30
            or density_variance > 0.4,
            "volatility_score": (
                risk_variance + satisfaction_variance / 100 + density_variance
            )
            / 3,
        }

    def get_recommended_branch_focus(self) -> str:
        """Determine which branch requires most attention"""
        if not self.most_likely:
            return "insufficient_data"

        if self.worst_case and self.worst_case.overall_risk_score > 0.7:
            return "worst_case_mitigation"

        if self.best_case and self.most_likely.overall_satisfaction_score < 60:
            return "satisfaction_improvement"

        if self.variance_analysis.get("high_variance", False):
            return "scenario_stabilization"

        return "most_likely_optimization"

    def to_dict(self) -> Dict[str, Any]:
        """Convert branch set to dictionary"""
        return {
            "prediction_id": self.prediction_id,
            "scenario_name": self.scenario_name,
            "trigger_context": self.trigger_context,
            "branches": {
                "best_case": self.best_case.to_dict() if self.best_case else None,
                "most_likely": self.most_likely.to_dict() if self.most_likely else None,
                "worst_case": self.worst_case.to_dict() if self.worst_case else None,
            },
            "analysis": {
                "variance_analysis": self.variance_analysis,
                "decision_impact_analysis": self.decision_impact_analysis,
                "recommended_focus": self.get_recommended_branch_focus(),
            },
            "generated_at": self.generated_at.isoformat(),
        }
