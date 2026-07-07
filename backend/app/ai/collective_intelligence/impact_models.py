"""
StadiumVerse AI V2 - Impact Assessment Models
Data structures for measuring intervention impacts and ROI
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid

class InterventionType(str, Enum):
    VOLUNTEER_DEPLOYMENT = "volunteer_deployment"
    GATE_OPERATION = "gate_operation"
    QUEUE_MANAGEMENT = "queue_management"
    COMMUNICATION = "communication"
    RESOURCE_ALLOCATION = "resource_allocation"
    TRANSPORT_ADJUSTMENT = "transport_adjustment"
    FACILITY_OPERATION = "facility_operation"
    EMERGENCY_PREPARATION = "emergency_preparation"

class ImpactCategory(str, Enum):
    FAN_SATISFACTION = "fan_satisfaction"
    WAIT_TIME_REDUCTION = "wait_time_reduction"
    SAFETY_IMPROVEMENT = "safety_improvement"
    REVENUE_INCREASE = "revenue_increase"
    CARBON_REDUCTION = "carbon_reduction"
    EFFICIENCY_GAIN = "efficiency_gain"
    RISK_MITIGATION = "risk_mitigation"
    ACCESSIBILITY_ENHANCEMENT = "accessibility_enhancement"

@dataclass
class ROIAnalysis:
    """Return on Investment analysis for interventions"""
    
    # Cost factors
    resource_cost: float = 0.0  # Direct resource cost ($)
    time_cost: float = 0.0  # Opportunity cost of time ($)
    personnel_cost: float = 0.0  # Staff time cost ($)
    system_cost: float = 0.0  # System/technology cost ($)
    
    # Benefit factors
    revenue_benefit: float = 0.0  # Direct revenue increase ($)
    efficiency_benefit: float = 0.0  # Efficiency savings ($)
    satisfaction_benefit: float = 0.0  # Fan satisfaction value ($)
    risk_mitigation_benefit: float = 0.0  # Risk reduction value ($)
    carbon_benefit: float = 0.0  # Carbon reduction value ($)
    
    # Analysis results
    total_cost: float = field(init=False)
    total_benefit: float = field(init=False)
    net_benefit: float = field(init=False)
    roi_ratio: float = field(init=False)
    payback_period_minutes: float = field(init=False)
    
    def __post_init__(self):
        self.total_cost = (
            self.resource_cost + self.time_cost + 
            self.personnel_cost + self.system_cost
        )
        
        self.total_benefit = (
            self.revenue_benefit + self.efficiency_benefit + 
            self.satisfaction_benefit + self.risk_mitigation_benefit + 
            self.carbon_benefit
        )
        
        self.net_benefit = self.total_benefit - self.total_cost
        
        self.roi_ratio = (
            self.total_benefit / self.total_cost 
            if self.total_cost > 0 else float('inf')
        )
        
        # Estimate payback period (simplified)
        if self.total_benefit > self.total_cost:
            # Assume benefit accrual over 2 hours
            benefit_per_minute = self.total_benefit / 120
            self.payback_period_minutes = (
                self.total_cost / benefit_per_minute 
                if benefit_per_minute > 0 else 120
            )
        else:
            self.payback_period_minutes = float('inf')
    
    def get_roi_category(self) -> str:
        """Categorize ROI performance"""
        if self.roi_ratio >= 3.0:
            return "excellent"
        elif self.roi_ratio >= 2.0:
            return "very_good"
        elif self.roi_ratio >= 1.5:
            return "good"
        elif self.roi_ratio >= 1.0:
            return "positive"
        else:
            return "negative"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "costs": {
                "resource_cost": self.resource_cost,
                "time_cost": self.time_cost,
                "personnel_cost": self.personnel_cost,
                "system_cost": self.system_cost,
                "total_cost": self.total_cost
            },
            "benefits": {
                "revenue_benefit": self.revenue_benefit,
                "efficiency_benefit": self.efficiency_benefit,
                "satisfaction_benefit": self.satisfaction_benefit,
                "risk_mitigation_benefit": self.risk_mitigation_benefit,
                "carbon_benefit": self.carbon_benefit,
                "total_benefit": self.total_benefit
            },
            "analysis": {
                "net_benefit": self.net_benefit,
                "roi_ratio": self.roi_ratio,
                "roi_category": self.get_roi_category(),
                "payback_period_minutes": self.payback_period_minutes
            }
        }

@dataclass
class ImpactAssessment:
    """Assessment of intervention impact across multiple categories"""
    
    category: ImpactCategory
    current_baseline: float
    predicted_improvement: float
    confidence: float  # 0.0 to 1.0
    
    # Quantified impacts
    fans_affected: int = 0
    time_to_impact_minutes: int = 5
    impact_duration_minutes: int = 60
    measurable_metrics: Dict[str, float] = field(default_factory=dict)
    
    # Qualitative assessment
    impact_description: str = ""
    success_indicators: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    
    def calculate_impact_magnitude(self) -> float:
        """Calculate overall impact magnitude (0.0 to 1.0)"""
        # Base impact from improvement percentage
        improvement_factor = abs(self.predicted_improvement - self.current_baseline) / 100.0
        
        # Scale by number of fans affected (log scale to prevent domination)
        if self.fans_affected > 0:
            fan_factor = min(1.0, math.log10(self.fans_affected) / 5.0)  # Log scale
        else:
            fan_factor = 0.1
        
        # Weight by confidence
        confidence_factor = self.confidence
        
        # Duration factor (longer impact = higher magnitude)
        duration_factor = min(1.0, self.impact_duration_minutes / 120.0)  # 2 hours = max
        
        magnitude = (
            improvement_factor * 0.4 + 
            fan_factor * 0.3 + 
            confidence_factor * 0.2 + 
            duration_factor * 0.1
        )
        
        return min(1.0, max(0.0, magnitude))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category.value,
            "current_baseline": self.current_baseline,
            "predicted_improvement": self.predicted_improvement,
            "improvement_delta": self.predicted_improvement - self.current_baseline,
            "confidence": self.confidence,
            "fans_affected": self.fans_affected,
            "time_to_impact_minutes": self.time_to_impact_minutes,
            "impact_duration_minutes": self.impact_duration_minutes,
            "impact_magnitude": self.calculate_impact_magnitude(),
            "measurable_metrics": self.measurable_metrics,
            "impact_description": self.impact_description,
            "success_indicators": self.success_indicators,
            "risk_factors": self.risk_factors
        }

@dataclass
class InterventionProposal:
    """A specific intervention proposal with full impact and ROI analysis"""
    
    proposal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    intervention_type: InterventionType = InterventionType.VOLUNTEER_DEPLOYMENT
    
    # Implementation details
    specific_actions: List[str] = field(default_factory=list)
    resource_requirements: List[str] = field(default_factory=list)
    implementation_steps: List[str] = field(default_factory=list)
    estimated_implementation_time: int = 5  # minutes
    
    # Impact analysis
    impact_assessments: List[ImpactAssessment] = field(default_factory=list)
    roi_analysis: Optional[ROIAnalysis] = None
    
    # Decision support
    urgency_score: float = 0.5  # 0.0 to 1.0
    complexity_score: float = 0.3  # 0.0 to 1.0 (lower = easier)
    success_probability: float = 0.8  # 0.0 to 1.0
    
    # Context and reasoning
    trigger_context: Dict[str, Any] = field(default_factory=dict)
    ai_reasoning: str = ""
    alternative_options: List[str] = field(default_factory=list)
    
    # Tracking
    generated_at: datetime = field(default_factory=datetime.utcnow)
    valid_until: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=30))
    
    def add_impact_assessment(self, assessment: ImpactAssessment):
        """Add an impact assessment to this proposal"""
        self.impact_assessments.append(assessment)
    
    def calculate_overall_impact_score(self) -> float:
        """Calculate overall impact score across all categories"""
        if not self.impact_assessments:
            return 0.0
        
        # Weight different impact categories
        category_weights = {
            ImpactCategory.SAFETY_IMPROVEMENT: 0.25,
            ImpactCategory.FAN_SATISFACTION: 0.20,
            ImpactCategory.WAIT_TIME_REDUCTION: 0.15,
            ImpactCategory.EFFICIENCY_GAIN: 0.15,
            ImpactCategory.RISK_MITIGATION: 0.10,
            ImpactCategory.REVENUE_INCREASE: 0.10,
            ImpactCategory.CARBON_REDUCTION: 0.03,
            ImpactCategory.ACCESSIBILITY_ENHANCEMENT: 0.02
        }
        
        weighted_score = 0.0
        total_weight = 0.0
        
        for assessment in self.impact_assessments:
            weight = category_weights.get(assessment.category, 0.1)
            magnitude = assessment.calculate_impact_magnitude()
            weighted_score += magnitude * weight * assessment.confidence
            total_weight += weight
        
        return weighted_score / total_weight if total_weight > 0 else 0.0
    
    def calculate_intervention_efficiency(self) -> float:
        """Calculate efficiency: impact per unit of effort/cost"""
        impact_score = self.calculate_overall_impact_score()
        
        # Efficiency factors
        time_efficiency = 1.0 / max(1, self.estimated_implementation_time / 10.0)  # 10 min baseline
        complexity_efficiency = 1.0 - self.complexity_score
        
        if self.roi_analysis and self.roi_analysis.total_cost > 0:
            cost_efficiency = self.roi_analysis.total_benefit / self.roi_analysis.total_cost
        else:
            cost_efficiency = 1.0
        
        # Combined efficiency score
        efficiency = (
            impact_score * 0.5 + 
            time_efficiency * 0.2 + 
            complexity_efficiency * 0.2 + 
            min(2.0, cost_efficiency) * 0.1  # Cap cost efficiency at 2.0
        )
        
        return min(1.0, efficiency)
    
    def get_priority_score(self) -> float:
        """Calculate overall priority score for ranking interventions"""
        impact = self.calculate_overall_impact_score()
        efficiency = self.calculate_intervention_efficiency()
        urgency = self.urgency_score
        success_prob = self.success_probability
        
        # Weighted priority calculation
        priority = (
            impact * 0.35 +
            efficiency * 0.25 + 
            urgency * 0.25 +
            success_prob * 0.15
        )
        
        return min(1.0, max(0.0, priority))
    
    def get_total_fans_affected(self) -> int:
        """Get total number of fans affected across all impact categories"""
        return sum(assessment.fans_affected for assessment in self.impact_assessments)
    
    def get_expected_implementation_timeline(self) -> Dict[str, str]:
        """Generate implementation timeline"""
        start_time = datetime.utcnow()
        
        timeline = {
            "start_time": start_time.strftime("%H:%M"),
            "preparation_complete": (start_time + timedelta(minutes=2)).strftime("%H:%M"),
            "implementation_start": (start_time + timedelta(minutes=3)).strftime("%H:%M"),
            "full_effect": (start_time + timedelta(minutes=self.estimated_implementation_time + 5)).strftime("%H:%M"),
            "assessment_available": (start_time + timedelta(minutes=self.estimated_implementation_time + 15)).strftime("%H:%M")
        }
        
        return timeline
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert proposal to dictionary for API responses"""
        return {
            "proposal_id": self.proposal_id,
            "title": self.title,
            "description": self.description,
            "intervention_type": self.intervention_type.value,
            
            "implementation": {
                "specific_actions": self.specific_actions,
                "resource_requirements": self.resource_requirements,
                "implementation_steps": self.implementation_steps,
                "estimated_implementation_time": self.estimated_implementation_time,
                "timeline": self.get_expected_implementation_timeline()
            },
            
            "impact_analysis": {
                "assessments": [assessment.to_dict() for assessment in self.impact_assessments],
                "overall_impact_score": self.calculate_overall_impact_score(),
                "total_fans_affected": self.get_total_fans_affected(),
                "roi_analysis": self.roi_analysis.to_dict() if self.roi_analysis else None
            },
            
            "decision_factors": {
                "priority_score": self.get_priority_score(),
                "urgency_score": self.urgency_score,
                "complexity_score": self.complexity_score,
                "success_probability": self.success_probability,
                "intervention_efficiency": self.calculate_intervention_efficiency()
            },
            
            "reasoning": {
                "ai_reasoning": self.ai_reasoning,
                "alternative_options": self.alternative_options,
                "trigger_context": self.trigger_context
            },
            
            "metadata": {
                "generated_at": self.generated_at.isoformat(),
                "valid_until": self.valid_until.isoformat()
            }
        }

import math  # Add this import at the top