"""
StadiumVerse AI V2 - Intervention Calculator
Calculates optimal interventions with maximum ROI and minimal resource usage
"""

import asyncio
import logging
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

from .impact_models import (
    InterventionProposal, ImpactAssessment, ROIAnalysis, 
    InterventionType, ImpactCategory
)
from ..providers.factory import get_global_ai_provider

logger = logging.getLogger(__name__)

@dataclass
class InterventionMetrics:
    """Metrics for evaluating intervention effectiveness"""
    cost_per_fan: float
    time_to_implement: int  # minutes
    resource_intensity: float  # 0.0 to 1.0
    disruption_level: float  # 0.0 to 1.0
    success_probability: float  # 0.0 to 1.0
    cascading_effects: Dict[str, float]

class InterventionCalculator:
    """
    Advanced calculator for intervention analysis and optimization
    Finds the smallest changes with the biggest positive impact
    """
    
    def __init__(self):
        self.intervention_history = []
        self.success_patterns = {}
        self.failure_patterns = {}
        
        # Cost and impact baselines
        self.resource_costs = {
            InterventionType.VOLUNTEER_DEPLOYMENT: {"cost": 15.0, "time": 3, "disruption": 0.1},
            InterventionType.GATE_OPERATION: {"cost": 5.0, "time": 2, "disruption": 0.3},
            InterventionType.QUEUE_MANAGEMENT: {"cost": 8.0, "time": 4, "disruption": 0.2},
            InterventionType.COMMUNICATION: {"cost": 2.0, "time": 1, "disruption": 0.05},
            InterventionType.RESOURCE_ALLOCATION: {"cost": 12.0, "time": 5, "disruption": 0.15},
            InterventionType.TRANSPORT_ADJUSTMENT: {"cost": 20.0, "time": 8, "disruption": 0.4},
            InterventionType.FACILITY_OPERATION: {"cost": 10.0, "time": 6, "disruption": 0.25},
            InterventionType.EMERGENCY_PREPARATION: {"cost": 25.0, "time": 10, "disruption": 0.1}
        }
        
        # Impact multipliers for different categories
        self.impact_multipliers = {
            ImpactCategory.SAFETY_IMPROVEMENT: 3.0,
            ImpactCategory.FAN_SATISFACTION: 2.0,
            ImpactCategory.WAIT_TIME_REDUCTION: 1.8,
            ImpactCategory.EFFICIENCY_GAIN: 1.5,
            ImpactCategory.RISK_MITIGATION: 2.5,
            ImpactCategory.REVENUE_INCREASE: 1.2,
            ImpactCategory.CARBON_REDUCTION: 1.1,
            ImpactCategory.ACCESSIBILITY_ENHANCEMENT: 2.2
        }
        
        logger.info("InterventionCalculator initialized with baseline metrics")
    
    async def calculate_intervention_metrics(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any]
    ) -> InterventionMetrics:
        """Calculate comprehensive metrics for an intervention proposal"""
        
        # Get baseline costs for intervention type
        baseline = self.resource_costs.get(
            proposal.intervention_type, 
            {"cost": 10.0, "time": 5, "disruption": 0.2}
        )
        
        # Calculate cost per affected fan
        total_affected = proposal.get_total_fans_affected()
        cost_per_fan = baseline["cost"] / max(1, total_affected)
        
        # Calculate resource intensity based on requirements
        resource_intensity = len(proposal.resource_requirements) * 0.1
        resource_intensity += proposal.complexity_score * 0.5
        resource_intensity = min(1.0, resource_intensity)
        
        # Calculate disruption level
        disruption_level = baseline["disruption"]
        if proposal.urgency_score > 0.8:
            disruption_level *= 1.5  # High urgency increases disruption
        
        # Analyze cascading effects
        cascading_effects = await self._analyze_cascading_effects(proposal, current_state)
        
        return InterventionMetrics(
            cost_per_fan=cost_per_fan,
            time_to_implement=proposal.estimated_implementation_time,
            resource_intensity=resource_intensity,
            disruption_level=disruption_level,
            success_probability=proposal.success_probability,
            cascading_effects=cascading_effects
        )
    
    async def _analyze_cascading_effects(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any]
    ) -> Dict[str, float]:
        """Analyze potential cascading effects of an intervention"""
        
        ai_provider = await get_global_ai_provider()
        
        cascading_prompt = f"""
CASCADING EFFECTS ANALYSIS

Intervention: {proposal.title}
Type: {proposal.intervention_type.value}
Description: {proposal.description}

Current Stadium State:
- Total Fans: {current_state.get('total_fans', 'Unknown')}
- Avg Stress Level: {current_state.get('avg_stress_level', 'Unknown')}
- Available Volunteers: {current_state.get('available_volunteers', 'Unknown')}
- Active Emergencies: {current_state.get('active_emergencies', 0)}

Analyze the potential cascading effects of this intervention:
1. Positive cascading effects (improvements that trigger other improvements)
2. Negative cascading effects (unintended consequences)
3. Resource strain effects (impact on other stadium operations)
4. Timeline effects (how effects compound over time)

Provide numerical estimates (0.0 to 1.0) for:
- Queue reduction cascade
- Staff efficiency cascade  
- Fan satisfaction cascade
- Safety improvement cascade
- Revenue impact cascade
- Resource strain cascade

Be specific and quantitative in your analysis.
"""
        
        try:
            response = await ai_provider.generate_agent_response(
                agent_name="intervention_calculator",
                system_prompt=self._get_calculator_prompt(),
                user_message=cascading_prompt,
                context={"proposal": proposal.to_dict(), "state": current_state}
            )
            
            return self._parse_cascading_effects(response.content)
            
        except Exception as e:
            logger.error(f"Error analyzing cascading effects: {e}")
            return self._default_cascading_effects()
    
    def _parse_cascading_effects(self, ai_response: str) -> Dict[str, float]:
        """Parse AI response for cascading effects"""
        effects = {
            "queue_reduction": 0.0,
            "staff_efficiency": 0.0,
            "fan_satisfaction": 0.0,
            "safety_improvement": 0.0,
            "revenue_impact": 0.0,
            "resource_strain": 0.0
        }
        
        lines = ai_response.lower().split('\n')
        
        for line in lines:
            for effect_key in effects.keys():
                if effect_key.replace('_', ' ') in line:
                    # Extract numeric value
                    import re
                    numbers = re.findall(r'0\.\d+|\d+(?:\.\d+)?', line)
                    if numbers:
                        value = float(numbers[0])
                        # Normalize to 0.0-1.0 range
                        if value > 1.0:
                            value = value / 100.0 if value <= 100 else 1.0
                        effects[effect_key] = min(1.0, max(0.0, value))
                        break
        
        return effects
    
    def _default_cascading_effects(self) -> Dict[str, float]:
        """Default cascading effects when AI analysis fails"""
        return {
            "queue_reduction": 0.3,
            "staff_efficiency": 0.2,
            "fan_satisfaction": 0.4,
            "safety_improvement": 0.2,
            "revenue_impact": 0.1,
            "resource_strain": 0.3
        }
    
    def calculate_intervention_roi(
        self,
        proposal: InterventionProposal,
        metrics: InterventionMetrics,
        current_state: Dict[str, Any]
    ) -> ROIAnalysis:
        """Calculate detailed ROI analysis for intervention"""
        
        # Calculate costs
        resource_cost = metrics.cost_per_fan * proposal.get_total_fans_affected()
        personnel_cost = metrics.time_to_implement * 0.5  # $0.50 per minute
        time_cost = metrics.time_to_implement * 0.2  # Opportunity cost
        system_cost = metrics.resource_intensity * 10.0  # System resource usage
        
        # Calculate benefits based on impact assessments
        revenue_benefit = self._calculate_revenue_benefit(proposal, metrics, current_state)
        efficiency_benefit = self._calculate_efficiency_benefit(proposal, metrics, current_state)
        satisfaction_benefit = self._calculate_satisfaction_benefit(proposal, metrics, current_state)
        risk_mitigation_benefit = self._calculate_risk_benefit(proposal, metrics, current_state)
        carbon_benefit = self._calculate_carbon_benefit(proposal, metrics, current_state)
        
        # Apply cascading effect multipliers
        cascading_multiplier = 1.0 + sum(metrics.cascading_effects.values()) / 6.0
        
        return ROIAnalysis(
            resource_cost=resource_cost,
            time_cost=time_cost,
            personnel_cost=personnel_cost,
            system_cost=system_cost,
            revenue_benefit=revenue_benefit * cascading_multiplier,
            efficiency_benefit=efficiency_benefit * cascading_multiplier,
            satisfaction_benefit=satisfaction_benefit * cascading_multiplier,
            risk_mitigation_benefit=risk_mitigation_benefit * cascading_multiplier,
            carbon_benefit=carbon_benefit * cascading_multiplier
        )
    
    def _calculate_revenue_benefit(
        self,
        proposal: InterventionProposal,
        metrics: InterventionMetrics,
        current_state: Dict[str, Any]
    ) -> float:
        """Calculate potential revenue benefit"""
        
        # Find revenue-related impact assessments
        revenue_impacts = [
            assessment for assessment in proposal.impact_assessments
            if assessment.category in [ImpactCategory.REVENUE_INCREASE, ImpactCategory.EFFICIENCY_GAIN]
        ]
        
        if not revenue_impacts:
            # Estimate based on fan satisfaction and efficiency
            base_revenue_per_fan = 25.0  # Average spending
            affected_fans = proposal.get_total_fans_affected()
            satisfaction_boost = metrics.cascading_effects.get("fan_satisfaction", 0.2)
            
            return affected_fans * base_revenue_per_fan * satisfaction_boost * 0.1
        
        # Calculate from impact assessments
        total_benefit = 0.0
        for impact in revenue_impacts:
            improvement = abs(impact.predicted_improvement - impact.current_baseline)
            fan_value = impact.fans_affected * 25.0  # Base spending per fan
            improvement_factor = improvement / 100.0  # Convert percentage
            
            benefit = fan_value * improvement_factor * impact.confidence
            total_benefit += benefit
        
        return total_benefit
    
    def _calculate_efficiency_benefit(
        self,
        proposal: InterventionProposal,
        metrics: InterventionMetrics,
        current_state: Dict[str, Any]
    ) -> float:
        """Calculate operational efficiency benefit"""
        
        # Time savings value
        time_saved_minutes = 0.0
        for impact in proposal.impact_assessments:
            if impact.category == ImpactCategory.WAIT_TIME_REDUCTION:
                improvement = abs(impact.predicted_improvement - impact.current_baseline)
                time_saved_minutes += improvement * impact.fans_affected
        
        # Value time savings at $0.20 per fan per minute saved
        time_value = time_saved_minutes * 0.20
        
        # Staff efficiency improvements
        staff_efficiency = metrics.cascading_effects.get("staff_efficiency", 0.2)
        staff_benefit = staff_efficiency * 100.0  # $100 value per efficiency point
        
        return time_value + staff_benefit
    
    def _calculate_satisfaction_benefit(
        self,
        proposal: InterventionProposal,
        metrics: InterventionMetrics,
        current_state: Dict[str, Any]
    ) -> float:
        """Calculate fan satisfaction benefit (monetized)"""
        
        satisfaction_impacts = [
            impact for impact in proposal.impact_assessments
            if impact.category == ImpactCategory.FAN_SATISFACTION
        ]
        
        if not satisfaction_impacts:
            # Estimate based on affected fans and type of intervention
            affected_fans = proposal.get_total_fans_affected()
            satisfaction_value_per_fan = 5.0  # $5 value per satisfaction point
            estimated_improvement = 0.1  # 10% improvement
            
            return affected_fans * satisfaction_value_per_fan * estimated_improvement
        
        total_benefit = 0.0
        for impact in satisfaction_impacts:
            improvement = abs(impact.predicted_improvement - impact.current_baseline)
            benefit = impact.fans_affected * 5.0 * (improvement / 100.0) * impact.confidence
            total_benefit += benefit
        
        return total_benefit
    
    def _calculate_risk_benefit(
        self,
        proposal: InterventionProposal,
        metrics: InterventionMetrics,
        current_state: Dict[str, Any]
    ) -> float:
        """Calculate risk mitigation benefit"""
        
        risk_impacts = [
            impact for impact in proposal.impact_assessments
            if impact.category in [ImpactCategory.RISK_MITIGATION, ImpactCategory.SAFETY_IMPROVEMENT]
        ]
        
        # Base risk mitigation value
        base_risk_value = 500.0  # Value of preventing one incident
        
        if not risk_impacts:
            # Estimate based on intervention type
            risk_reduction = {
                InterventionType.SECURITY_DEPLOYMENT: 0.3,
                InterventionType.EMERGENCY_PREPARATION: 0.4,
                InterventionType.MEDICAL_DEPLOYMENT: 0.35,
                InterventionType.CROWD_MANAGEMENT: 0.25
            }.get(proposal.intervention_type, 0.1)
            
            return base_risk_value * risk_reduction * metrics.success_probability
        
        total_benefit = 0.0
        for impact in risk_impacts:
            improvement = abs(impact.predicted_improvement - impact.current_baseline)
            risk_value = base_risk_value * (improvement / 100.0) * impact.confidence
            total_benefit += risk_value
        
        return total_benefit
    
    def _calculate_carbon_benefit(
        self,
        proposal: InterventionProposal,
        metrics: InterventionMetrics,
        current_state: Dict[str, Any]
    ) -> float:
        """Calculate carbon footprint reduction benefit"""
        
        carbon_impacts = [
            impact for impact in proposal.impact_assessments
            if impact.category == ImpactCategory.CARBON_REDUCTION
        ]
        
        carbon_price_per_ton = 25.0  # $25 per ton CO2 equivalent
        
        if not carbon_impacts:
            # Estimate based on intervention type
            carbon_savings_kg = {
                InterventionType.TRANSPORT_ADJUSTMENT: 50.0,
                InterventionType.RESOURCE_ALLOCATION: 20.0,
                InterventionType.FACILITY_OPERATION: 30.0
            }.get(proposal.intervention_type, 10.0)
            
            carbon_tons = carbon_savings_kg / 1000.0
            return carbon_tons * carbon_price_per_ton
        
        total_benefit = 0.0
        for impact in carbon_impacts:
            improvement = abs(impact.predicted_improvement - impact.current_baseline)
            carbon_tons = (improvement / 100.0) * 0.1  # Estimate tons from percentage
            benefit = carbon_tons * carbon_price_per_ton * impact.confidence
            total_benefit += benefit
        
        return total_benefit
    
    def calculate_intervention_efficiency_score(
        self,
        proposal: InterventionProposal,
        roi_analysis: ROIAnalysis,
        metrics: InterventionMetrics
    ) -> float:
        """Calculate overall intervention efficiency score"""
        
        # ROI component (40% weight)
        roi_component = min(1.0, roi_analysis.roi_ratio / 3.0) * 0.4
        
        # Time efficiency (20% weight)
        time_efficiency = max(0.0, 1.0 - (metrics.time_to_implement / 60.0)) * 0.2
        
        # Resource efficiency (20% weight)
        resource_efficiency = max(0.0, 1.0 - metrics.resource_intensity) * 0.2
        
        # Success probability (10% weight)
        success_component = metrics.success_probability * 0.1
        
        # Disruption penalty (10% weight)
        disruption_component = max(0.0, 1.0 - metrics.disruption_level) * 0.1
        
        efficiency_score = (
            roi_component + time_efficiency + resource_efficiency + 
            success_component + disruption_component
        )
        
        return min(1.0, max(0.0, efficiency_score))
    
    def rank_interventions_by_efficiency(
        self,
        proposals: List[InterventionProposal],
        current_state: Dict[str, Any]
    ) -> List[Tuple[InterventionProposal, float, InterventionMetrics, ROIAnalysis]]:
        """
        Rank multiple interventions by efficiency score
        Returns list of (proposal, efficiency_score, metrics, roi_analysis)
        """
        
        ranked_interventions = []
        
        for proposal in proposals:
            try:
                # This would need to be made async in real implementation
                # For now, using synchronous approach
                metrics = self._calculate_basic_metrics(proposal, current_state)
                roi_analysis = self.calculate_intervention_roi(proposal, metrics, current_state)
                efficiency_score = self.calculate_intervention_efficiency_score(proposal, roi_analysis, metrics)
                
                ranked_interventions.append((proposal, efficiency_score, metrics, roi_analysis))
                
            except Exception as e:
                logger.error(f"Error calculating efficiency for proposal {proposal.proposal_id}: {e}")
                continue
        
        # Sort by efficiency score (descending)
        ranked_interventions.sort(key=lambda x: x[1], reverse=True)
        
        return ranked_interventions
    
    def _calculate_basic_metrics(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any]
    ) -> InterventionMetrics:
        """Calculate basic metrics without AI analysis (synchronous version)"""
        
        baseline = self.resource_costs.get(
            proposal.intervention_type,
            {"cost": 10.0, "time": 5, "disruption": 0.2}
        )
        
        total_affected = proposal.get_total_fans_affected()
        cost_per_fan = baseline["cost"] / max(1, total_affected)
        
        resource_intensity = len(proposal.resource_requirements) * 0.1
        resource_intensity += proposal.complexity_score * 0.5
        resource_intensity = min(1.0, resource_intensity)
        
        disruption_level = baseline["disruption"]
        if proposal.urgency_score > 0.8:
            disruption_level *= 1.5
        
        # Default cascading effects
        cascading_effects = self._default_cascading_effects()
        
        return InterventionMetrics(
            cost_per_fan=cost_per_fan,
            time_to_implement=proposal.estimated_implementation_time,
            resource_intensity=resource_intensity,
            disruption_level=disruption_level,
            success_probability=proposal.success_probability,
            cascading_effects=cascading_effects
        )
    
    def _get_calculator_prompt(self) -> str:
        """System prompt for intervention calculator AI agent"""
        return """
You are the Intervention Calculator for StadiumVerse AI's collective intelligence system.

Your expertise is quantitative analysis of stadium interventions, focusing on:
1. Cost-benefit analysis and ROI calculations
2. Resource optimization and efficiency metrics
3. Cascading effect analysis and system interactions
4. Risk assessment and mitigation strategies
5. Time-based impact modeling

Provide specific, quantitative analysis with:
- Numerical estimates and confidence intervals
- Clear reasoning for calculations
- Identification of key variables and assumptions
- Risk factors and uncertainty bounds
- Alternative scenarios and sensitivities

Always consider both direct and indirect effects of interventions.
Focus on measurable outcomes and practical implementation constraints.
"""
    
    def record_intervention_outcome(
        self,
        proposal_id: str,
        actual_outcome: Dict[str, Any],
        success: bool
    ):
        """Record the outcome of an intervention for learning"""
        
        outcome_record = {
            "proposal_id": proposal_id,
            "timestamp": datetime.utcnow().isoformat(),
            "actual_outcome": actual_outcome,
            "success": success
        }
        
        self.intervention_history.append(outcome_record)
        
        # Update success/failure patterns for learning
        if success:
            self._update_success_patterns(actual_outcome)
        else:
            self._update_failure_patterns(actual_outcome)
        
        # Keep history manageable (last 1000 records)
        if len(self.intervention_history) > 1000:
            self.intervention_history = self.intervention_history[-1000:]
    
    def _update_success_patterns(self, outcome: Dict[str, Any]):
        """Update patterns that lead to successful interventions"""
        intervention_type = outcome.get("intervention_type")
        if intervention_type:
            if intervention_type not in self.success_patterns:
                self.success_patterns[intervention_type] = {"count": 0, "factors": {}}
            
            self.success_patterns[intervention_type]["count"] += 1
            
            # Update success factors
            for key, value in outcome.items():
                if key not in self.success_patterns[intervention_type]["factors"]:
                    self.success_patterns[intervention_type]["factors"][key] = []
                
                if isinstance(value, (int, float)):
                    self.success_patterns[intervention_type]["factors"][key].append(value)
    
    def _update_failure_patterns(self, outcome: Dict[str, Any]):
        """Update patterns that lead to failed interventions"""
        intervention_type = outcome.get("intervention_type")
        if intervention_type:
            if intervention_type not in self.failure_patterns:
                self.failure_patterns[intervention_type] = {"count": 0, "factors": {}}
            
            self.failure_patterns[intervention_type]["count"] += 1
            
            # Update failure factors
            for key, value in outcome.items():
                if key not in self.failure_patterns[intervention_type]["factors"]:
                    self.failure_patterns[intervention_type]["factors"][key] = []
                
                if isinstance(value, (int, float)):
                    self.failure_patterns[intervention_type]["factors"][key].append(value)
    
    def get_learning_insights(self) -> Dict[str, Any]:
        """Get insights from historical intervention data"""
        insights = {
            "total_interventions": len(self.intervention_history),
            "success_rate": 0.0,
            "most_successful_types": [],
            "common_failure_factors": [],
            "efficiency_trends": {}
        }
        
        if not self.intervention_history:
            return insights
        
        # Calculate overall success rate
        successes = sum(1 for record in self.intervention_history if record["success"])
        insights["success_rate"] = successes / len(self.intervention_history)
        
        # Identify most successful intervention types
        type_success_rates = {}
        for pattern_type, data in self.success_patterns.items():
            total_attempts = data["count"] + self.failure_patterns.get(pattern_type, {}).get("count", 0)
            success_rate = data["count"] / total_attempts if total_attempts > 0 else 0
            type_success_rates[pattern_type] = success_rate
        
        insights["most_successful_types"] = sorted(
            type_success_rates.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return insights