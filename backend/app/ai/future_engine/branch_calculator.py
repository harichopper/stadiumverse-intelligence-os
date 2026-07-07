"""
StadiumVerse AI V2 - Branch Calculator
Calculates best/likely/worst future scenarios using AI and data modeling
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math
import random

from .scenario_models import (
    FutureBranch, BranchType, TimelinePoint, ScenarioOutcome, 
    OutcomeCategory, FutureBranchSet
)
from ..providers.factory import get_global_ai_provider
from ...config import settings

logger = logging.getLogger(__name__)

class BranchCalculator:
    """
    Calculates multiple future scenarios using AI reasoning and statistical modeling
    """
    
    def __init__(self):
        self.calculation_depth = getattr(settings, 'BRANCH_CALCULATION_DEPTH', 6)
        self.confidence_threshold = getattr(settings, 'CONFIDENCE_THRESHOLD', 0.6)
        
    async def calculate_future_branches(
        self,
        current_state: Dict[str, Any],
        scenario_context: Dict[str, Any],
        prediction_horizon_minutes: int = 30
    ) -> FutureBranchSet:
        """
        Calculate all three future branches (best/likely/worst) for given scenario
        
        Args:
            current_state: Current stadium state data
            scenario_context: Context about the scenario being analyzed
            prediction_horizon_minutes: How far into future to predict
            
        Returns:
            FutureBranchSet: Complete set of future branches
        """
        logger.info(f"Calculating future branches for {prediction_horizon_minutes} minute horizon")
        
        branch_set = FutureBranchSet(
            scenario_name=scenario_context.get("name", "Stadium Analysis"),
            trigger_context=scenario_context
        )
        
        # Calculate all three branches concurrently for efficiency
        branch_tasks = [
            self._calculate_single_branch(
                BranchType.BEST_CASE, 
                current_state, 
                scenario_context, 
                prediction_horizon_minutes
            ),
            self._calculate_single_branch(
                BranchType.MOST_LIKELY, 
                current_state, 
                scenario_context, 
                prediction_horizon_minutes
            ),
            self._calculate_single_branch(
                BranchType.WORST_CASE, 
                current_state, 
                scenario_context, 
                prediction_horizon_minutes
            )
        ]
        
        try:
            branches = await asyncio.gather(*branch_tasks)
            
            for branch in branches:
                if branch:
                    branch_set.add_branch(branch)
            
            # Calculate comparative analysis
            branch_set.calculate_variance_analysis()
            branch_set.decision_impact_analysis = await self._calculate_decision_impact(branch_set)
            
            return branch_set
            
        except Exception as e:
            logger.error(f"Error calculating future branches: {e}")
            
            # Return minimal branch set with error information
            fallback_branch = self._create_fallback_branch(
                BranchType.MOST_LIKELY, 
                current_state, 
                str(e)
            )
            branch_set.add_branch(fallback_branch)
            return branch_set
    
    async def _calculate_single_branch(
        self,
        branch_type: BranchType,
        current_state: Dict[str, Any],
        scenario_context: Dict[str, Any],
        horizon_minutes: int
    ) -> Optional[FutureBranch]:
        """Calculate a single future branch using AI analysis"""
        
        try:
            ai_provider = await get_global_ai_provider()
            
            # Create branch-specific analysis prompt
            analysis_prompt = self._create_branch_analysis_prompt(
                branch_type, 
                current_state, 
                scenario_context, 
                horizon_minutes
            )
            
            # Generate AI analysis
            response = await ai_provider.generate_agent_response(
                agent_name="future_predictor",
                system_prompt=self._get_future_predictor_prompt(),
                user_message=analysis_prompt
            )
            
            # Parse AI response into structured branch
            branch = await self._parse_ai_branch_response(
                branch_type,
                response.content,
                response.confidence,
                current_state,
                horizon_minutes
            )
            
            return branch
            
        except Exception as e:
            logger.error(f"Error calculating {branch_type.value} branch: {e}")
            return self._create_fallback_branch(branch_type, current_state, str(e))
    
    def _create_branch_analysis_prompt(
        self,
        branch_type: BranchType,
        current_state: Dict[str, Any],
        scenario_context: Dict[str, Any],
        horizon_minutes: int
    ) -> str:
        """Create AI prompt for branch-specific analysis"""
        
        branch_instructions = {
            BranchType.BEST_CASE: """
Analyze the BEST POSSIBLE outcome where:
- All systems work optimally
- No unexpected delays or problems
- Fans cooperate and follow guidance
- Weather and external factors are favorable
- Resources are used most efficiently
- All interventions succeed perfectly
""",
            BranchType.MOST_LIKELY: """
Analyze the MOST LIKELY outcome based on:
- Historical patterns and normal operations
- Typical fan behavior and response rates
- Standard resource efficiency levels  
- Expected minor delays and variations
- Realistic intervention success rates
- Normal external factor influences
""",
            BranchType.WORST_CASE: """
Analyze the WORST CASE scenario where:
- Multiple systems experience problems
- Delays compound and cascade
- Fans become frustrated or non-compliant
- External factors create additional stress
- Interventions are less effective
- Resource constraints become apparent
"""
        }
        
        current_metrics = self._format_current_metrics(current_state)
        scenario_desc = self._format_scenario_context(scenario_context)
        
        return f"""
FUTURE BRANCH ANALYSIS - {branch_type.value.upper().replace('_', ' ')}

{branch_instructions[branch_type]}

CURRENT STATE:
{current_metrics}

SCENARIO CONTEXT:
{scenario_desc}

PREDICTION HORIZON: {horizon_minutes} minutes

Provide detailed analysis with:

1. TIMELINE PREDICTIONS (every 5 minutes):
   - Crowd density (0-100%)
   - Average queue times (minutes)
   - Fan satisfaction (0-100)
   - Medical risk level (0-100%)
   - Revenue rate ($/minute)
   - Volunteer utilization (0-100%)
   - Key events at each timepoint

2. OUTCOME PREDICTIONS:
   - Crowd density impact and trends
   - Queue time changes and bottlenecks
   - Fan satisfaction factors
   - Medical incident predictions
   - Revenue impact assessment
   - Volunteer load distribution
   - Transport efficiency changes

3. CRITICAL FACTORS:
   - Key decisions that could change outcomes
   - Intervention opportunities
   - Risk mitigation strategies
   - Resource requirements

4. CONFIDENCE ASSESSMENT:
   - Overall confidence in predictions (0-100%)
   - Data quality and completeness
   - Uncertainty factors

Be specific with numbers, timeframes, and cause-effect relationships.
"""
    
    def _get_future_predictor_prompt(self) -> str:
        """System prompt for the future predictor agent"""
        return """
You are the Future Predictor for StadiumVerse AI's Living Brain system. Your expertise is in multi-scenario forecasting, temporal analysis, and predictive modeling for stadium operations.

Your role is to analyze current conditions and predict how they will evolve across different scenarios (best case, most likely, worst case).

Key principles:
1. Base predictions on data patterns and logical cause-effect chains
2. Consider fan psychology, crowd dynamics, and system interactions
3. Account for compounding effects and cascade scenarios
4. Provide specific, measurable predictions with timeframes
5. Identify intervention points and decision impact
6. Quantify confidence levels and uncertainty factors

Always structure your analysis with clear timeline points, outcome categories, and actionable insights.
"""
    
    async def _parse_ai_branch_response(
        self,
        branch_type: BranchType,
        ai_response: str,
        confidence: float,
        current_state: Dict[str, Any],
        horizon_minutes: int
    ) -> FutureBranch:
        """Parse AI response into structured FutureBranch"""
        
        # Create base branch
        branch = FutureBranch(
            branch_type=branch_type,
            title=self._generate_branch_title(branch_type),
            description=self._extract_description(ai_response),
            confidence_score=confidence
        )
        
        # Parse timeline points
        timeline_points = self._extract_timeline_points(ai_response, current_state, horizon_minutes)
        for point in timeline_points:
            branch.add_timeline_point(point)
        
        # Parse outcomes
        outcomes = self._extract_outcomes(ai_response, current_state)
        for outcome in outcomes:
            branch.add_outcome(outcome)
        
        # Extract strategic elements
        branch.critical_decisions = self._extract_critical_decisions(ai_response)
        branch.intervention_opportunities = self._extract_intervention_opportunities(ai_response)
        branch.risk_mitigation_strategies = self._extract_risk_strategies(ai_response)
        
        # Calculate overall scores
        branch.overall_risk_score = self._calculate_overall_risk_score(timeline_points)
        branch.overall_satisfaction_score = self._calculate_overall_satisfaction(timeline_points)
        branch.resource_efficiency_score = self._calculate_resource_efficiency(timeline_points)
        
        # Set probability based on branch type
        branch.probability = self._get_branch_probability(branch_type)
        
        return branch
    
    def _extract_timeline_points(
        self, 
        ai_response: str, 
        current_state: Dict[str, Any], 
        horizon_minutes: int
    ) -> List[TimelinePoint]:
        """Extract timeline predictions from AI response"""
        
        points = []
        base_time = datetime.utcnow()
        
        # Get current baseline values
        current_crowd = current_state.get("crowd_density", 0.5)
        current_queue = current_state.get("avg_queue_time", 5.0)
        current_satisfaction = current_state.get("fan_satisfaction", 75.0)
        
        # Generate timeline points every 5 minutes
        for minutes in range(0, horizon_minutes + 1, 5):
            timestamp = base_time + timedelta(minutes=minutes)
            
            # Extract or estimate values for this timepoint
            point_data = self._extract_timepoint_data(ai_response, minutes)
            
            # Apply trend modifiers based on branch type and time
            trend_modifier = self._calculate_trend_modifier(minutes, horizon_minutes)
            
            point = TimelinePoint(
                timestamp=timestamp,
                minutes_from_now=minutes,
                crowd_density=self._apply_bounds(
                    point_data.get("crowd_density", current_crowd) * trend_modifier, 0.0, 1.0
                ),
                avg_queue_time=max(0, point_data.get("queue_time", current_queue) * trend_modifier),
                fan_satisfaction=self._apply_bounds(
                    point_data.get("satisfaction", current_satisfaction), 0.0, 100.0
                ),
                medical_risk_level=self._apply_bounds(
                    point_data.get("medical_risk", 0.1), 0.0, 1.0
                ),
                revenue_rate=max(0, point_data.get("revenue_rate", 50.0)),
                carbon_output=max(0, point_data.get("carbon_output", 10.0)),
                volunteer_utilization=self._apply_bounds(
                    point_data.get("volunteer_util", 0.6), 0.0, 1.0
                ),
                transport_efficiency=self._apply_bounds(
                    point_data.get("transport_eff", 0.8), 0.0, 1.0
                ),
                key_events=point_data.get("events", [])
            )
            
            points.append(point)
        
        return points
    
    def _extract_timepoint_data(self, ai_response: str, minutes: int) -> Dict[str, Any]:
        """Extract data for a specific timepoint from AI response"""
        
        # Look for timepoint-specific data in AI response
        lines = ai_response.split('\n')
        timepoint_data = {}
        
        # Simple extraction - look for patterns like "5 minutes: crowd 80%"
        for line in lines:
            line = line.strip().lower()
            if f"{minutes} min" in line or f"t+{minutes}" in line:
                # Extract numerical values from this line
                import re
                
                # Crowd density
                crowd_match = re.search(r'crowd[^0-9]*(\d+)', line)
                if crowd_match:
                    timepoint_data["crowd_density"] = float(crowd_match.group(1)) / 100.0
                
                # Queue time
                queue_match = re.search(r'queue[^0-9]*(\d+)', line)
                if queue_match:
                    timepoint_data["queue_time"] = float(queue_match.group(1))
                
                # Satisfaction
                sat_match = re.search(r'satisfaction[^0-9]*(\d+)', line)
                if sat_match:
                    timepoint_data["satisfaction"] = float(sat_match.group(1))
        
        return timepoint_data
    
    def _extract_outcomes(self, ai_response: str, current_state: Dict[str, Any]) -> List[ScenarioOutcome]:
        """Extract outcome predictions from AI response"""
        outcomes = []
        
        # Define outcome mappings with default calculations
        outcome_mappings = {
            OutcomeCategory.CROWD_DENSITY: {
                "keywords": ["crowd", "density", "congestion"],
                "current_value": current_state.get("crowd_density", 0.5) * 100,
                "default_change": 10.0
            },
            OutcomeCategory.QUEUE_TIMES: {
                "keywords": ["queue", "wait", "line"],
                "current_value": current_state.get("avg_queue_time", 5.0),
                "default_change": 2.0
            },
            OutcomeCategory.FAN_SATISFACTION: {
                "keywords": ["satisfaction", "experience", "happy"],
                "current_value": current_state.get("fan_satisfaction", 75.0),
                "default_change": 5.0
            },
            OutcomeCategory.MEDICAL_INCIDENTS: {
                "keywords": ["medical", "health", "incident"],
                "current_value": current_state.get("medical_risk", 10.0),
                "default_change": 2.0
            },
            OutcomeCategory.REVENUE_IMPACT: {
                "keywords": ["revenue", "sales", "spending"],
                "current_value": current_state.get("revenue_rate", 100.0),
                "default_change": 15.0
            }
        }
        
        # Extract outcomes from AI response
        for category, mapping in outcome_mappings.items():
            predicted_value, confidence = self._extract_category_prediction(
                ai_response, 
                mapping["keywords"], 
                mapping["current_value"],
                mapping["default_change"]
            )
            
            change_pct = ((predicted_value - mapping["current_value"]) / mapping["current_value"]) * 100
            
            outcome = ScenarioOutcome(
                category=category,
                current_value=mapping["current_value"],
                predicted_value=predicted_value,
                change_percentage=change_pct,
                confidence=confidence,
                impact_description=self._generate_impact_description(category, change_pct),
                contributing_factors=self._extract_contributing_factors(ai_response, mapping["keywords"])
            )
            
            outcomes.append(outcome)
        
        return outcomes
    
    def _extract_category_prediction(
        self, 
        ai_response: str, 
        keywords: List[str], 
        current_value: float,
        default_change: float
    ) -> tuple[float, float]:
        """Extract prediction for a specific category from AI response"""
        
        lines = ai_response.lower().split('\n')
        prediction_value = current_value
        confidence = 0.6
        
        for line in lines:
            if any(keyword in line for keyword in keywords):
                # Try to extract numerical predictions
                import re
                numbers = re.findall(r'\d+(?:\.\d+)?', line)
                
                if numbers:
                    # Use the first reasonable number found
                    for num_str in numbers:
                        num = float(num_str)
                        if 0 <= num <= 200:  # Reasonable range for most metrics
                            prediction_value = num
                            confidence = 0.8
                            break
                    break
        
        # If no prediction found, apply default trend
        if prediction_value == current_value:
            prediction_value = current_value + default_change
            confidence = 0.5
        
        return prediction_value, confidence
    
    def _extract_critical_decisions(self, ai_response: str) -> List[str]:
        """Extract critical decisions from AI response"""
        decisions = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['decision', 'critical', 'key', 'important']):
                if len(line) > 20 and '?' not in line:  # Avoid questions
                    decisions.append(line[:100])  # Limit length
        
        # Default decisions if none found
        if not decisions:
            decisions = [
                "Monitor crowd density levels",
                "Adjust volunteer deployment", 
                "Optimize queue management"
            ]
        
        return decisions[:5]  # Max 5 decisions
    
    def _extract_intervention_opportunities(self, ai_response: str) -> List[str]:
        """Extract intervention opportunities from AI response"""
        opportunities = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['intervention', 'opportunity', 'improve', 'optimize']):
                if len(line) > 15:
                    opportunities.append(line[:100])
        
        if not opportunities:
            opportunities = [
                "Deploy additional volunteers",
                "Open alternative routes",
                "Implement queue management"
            ]
        
        return opportunities[:5]
    
    def _extract_risk_strategies(self, ai_response: str) -> List[str]:
        """Extract risk mitigation strategies from AI response"""
        strategies = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['mitigate', 'prevent', 'reduce', 'strategy']):
                if len(line) > 15:
                    strategies.append(line[:100])
        
        if not strategies:
            strategies = [
                "Increase monitoring frequency",
                "Prepare contingency resources",
                "Enhance communication protocols"
            ]
        
        return strategies[:5]
    
    def _calculate_overall_risk_score(self, timeline_points: List[TimelinePoint]) -> float:
        """Calculate overall risk score from timeline"""
        if not timeline_points:
            return 0.5
        
        risk_factors = []
        for point in timeline_points:
            # Combine various risk indicators
            point_risk = (
                point.crowd_density * 0.3 +
                point.medical_risk_level * 0.4 +
                min(1.0, point.avg_queue_time / 20.0) * 0.2 +
                (1.0 - point.transport_efficiency) * 0.1
            )
            risk_factors.append(point_risk)
        
        return sum(risk_factors) / len(risk_factors)
    
    def _calculate_overall_satisfaction(self, timeline_points: List[TimelinePoint]) -> float:
        """Calculate overall satisfaction score from timeline"""
        if not timeline_points:
            return 75.0
        
        satisfaction_scores = [point.fan_satisfaction for point in timeline_points]
        return sum(satisfaction_scores) / len(satisfaction_scores)
    
    def _calculate_resource_efficiency(self, timeline_points: List[TimelinePoint]) -> float:
        """Calculate resource efficiency score from timeline"""
        if not timeline_points:
            return 0.7
        
        efficiency_scores = []
        for point in timeline_points:
            # Balance utilization - not too low, not too high
            vol_efficiency = 1.0 - abs(point.volunteer_utilization - 0.7)
            transport_efficiency = point.transport_efficiency
            
            point_efficiency = (vol_efficiency + transport_efficiency) / 2
            efficiency_scores.append(point_efficiency)
        
        return sum(efficiency_scores) / len(efficiency_scores)
    
    def _generate_branch_title(self, branch_type: BranchType) -> str:
        """Generate descriptive title for branch"""
        titles = {
            BranchType.BEST_CASE: "Optimal Operations - Everything Goes Right",
            BranchType.MOST_LIKELY: "Expected Scenario - Normal Operations", 
            BranchType.WORST_CASE: "Challenging Conditions - Multiple Issues"
        }
        return titles[branch_type]
    
    def _extract_description(self, ai_response: str) -> str:
        """Extract scenario description from AI response"""
        # Take first substantial paragraph as description
        paragraphs = ai_response.split('\n\n')
        for para in paragraphs:
            if len(para) > 50 and not para.upper().isupper():
                return para[:300] + "..." if len(para) > 300 else para
        
        return "AI-generated scenario analysis based on current stadium conditions."
    
    def _extract_contributing_factors(self, ai_response: str, keywords: List[str]) -> List[str]:
        """Extract contributing factors for a specific category"""
        factors = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in keywords):
                if 'because' in line.lower() or 'due to' in line.lower():
                    factors.append(line[:80])
        
        return factors[:3]  # Max 3 factors
    
    def _generate_impact_description(self, category: OutcomeCategory, change_pct: float) -> str:
        """Generate natural language impact description"""
        
        magnitude = "significantly" if abs(change_pct) > 20 else "moderately" if abs(change_pct) > 10 else "slightly"
        direction = "increase" if change_pct > 0 else "decrease"
        
        descriptions = {
            OutcomeCategory.CROWD_DENSITY: f"Crowd density will {magnitude} {direction} by {abs(change_pct):.1f}%",
            OutcomeCategory.QUEUE_TIMES: f"Average wait times will {magnitude} {direction} by {abs(change_pct):.1f}%", 
            OutcomeCategory.FAN_SATISFACTION: f"Fan satisfaction will {magnitude} {direction} by {abs(change_pct):.1f}%",
            OutcomeCategory.MEDICAL_INCIDENTS: f"Medical risk levels will {magnitude} {direction} by {abs(change_pct):.1f}%",
            OutcomeCategory.REVENUE_IMPACT: f"Revenue generation will {magnitude} {direction} by {abs(change_pct):.1f}%"
        }
        
        return descriptions.get(category, f"Category will {magnitude} {direction}")
    
    def _get_branch_probability(self, branch_type: BranchType) -> float:
        """Get probability for branch type"""
        probabilities = {
            BranchType.BEST_CASE: 0.15,
            BranchType.MOST_LIKELY: 0.70,
            BranchType.WORST_CASE: 0.15
        }
        return probabilities[branch_type]
    
    def _calculate_trend_modifier(self, minutes: int, horizon_minutes: int) -> float:
        """Calculate trend modifier based on time progression"""
        # Linear progression with some randomness
        progress = minutes / horizon_minutes
        base_modifier = 1.0 + (progress * 0.3)  # 30% change over horizon
        
        # Add some randomness for realism
        randomness = random.uniform(-0.1, 0.1)
        
        return max(0.5, base_modifier + randomness)
    
    def _apply_bounds(self, value: float, min_val: float, max_val: float) -> float:
        """Apply bounds to a value"""
        return max(min_val, min(max_val, value))
    
    def _format_current_metrics(self, current_state: Dict[str, Any]) -> str:
        """Format current state metrics for AI prompt"""
        formatted = []
        
        metrics = {
            "Total Fans": current_state.get("total_fans", 0),
            "Crowd Density": f"{current_state.get('crowd_density', 0.5)*100:.0f}%",
            "Average Queue Time": f"{current_state.get('avg_queue_time', 5):.1f} minutes", 
            "Fan Satisfaction": f"{current_state.get('fan_satisfaction', 75):.0f}%",
            "Available Volunteers": current_state.get("available_volunteers", 0),
            "Active Emergencies": current_state.get("active_emergencies", 0),
            "Weather": current_state.get("weather", "Clear"),
            "Revenue Rate": f"${current_state.get('revenue_rate', 100):.0f}/minute"
        }
        
        for key, value in metrics.items():
            formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)
    
    def _format_scenario_context(self, scenario_context: Dict[str, Any]) -> str:
        """Format scenario context for AI prompt"""
        formatted = []
        
        for key, value in scenario_context.items():
            if isinstance(value, (str, int, float)):
                formatted.append(f"{key.title()}: {value}")
            elif isinstance(value, list):
                formatted.append(f"{key.title()}: {', '.join(map(str, value))}")
        
        return "\n".join(formatted) if formatted else "Standard operational scenario"
    
    def _create_fallback_branch(
        self, 
        branch_type: BranchType, 
        current_state: Dict[str, Any], 
        error_msg: str
    ) -> FutureBranch:
        """Create a fallback branch when AI generation fails"""
        
        branch = FutureBranch(
            branch_type=branch_type,
            title=f"Fallback {branch_type.value.replace('_', ' ').title()}",
            description=f"Simplified prediction due to processing error: {error_msg[:100]}",
            confidence_score=0.3
        )
        
        # Create basic timeline with current state extrapolation
        base_time = datetime.utcnow()
        current_crowd = current_state.get("crowd_density", 0.5)
        current_satisfaction = current_state.get("fan_satisfaction", 75.0)
        
        for minutes in range(0, 31, 10):  # Every 10 minutes for fallback
            point = TimelinePoint(
                timestamp=base_time + timedelta(minutes=minutes),
                minutes_from_now=minutes,
                crowd_density=min(1.0, current_crowd + (minutes * 0.01)),
                avg_queue_time=5.0 + (minutes * 0.2),
                fan_satisfaction=max(50.0, current_satisfaction - (minutes * 0.5)),
                medical_risk_level=0.1 + (minutes * 0.005),
                revenue_rate=50.0,
                carbon_output=10.0,
                volunteer_utilization=0.6,
                transport_efficiency=0.8,
                key_events=[f"Minute {minutes}: Status update"]
            )
            branch.add_timeline_point(point)
        
        # Set basic scores
        branch.overall_risk_score = 0.4
        branch.overall_satisfaction_score = 65.0
        branch.resource_efficiency_score = 0.6
        branch.probability = self._get_branch_probability(branch_type)
        
        return branch
    
    async def _calculate_decision_impact(self, branch_set: FutureBranchSet) -> Dict[str, Any]:
        """Calculate impact of potential decisions across branches"""
        
        branches = [b for b in [branch_set.best_case, branch_set.most_likely, branch_set.worst_case] if b]
        
        if not branches:
            return {}
        
        # Analyze common interventions across branches
        all_interventions = []
        for branch in branches:
            all_interventions.extend(branch.intervention_opportunities)
        
        # Find most common interventions
        intervention_counts = {}
        for intervention in all_interventions:
            intervention_counts[intervention] = intervention_counts.get(intervention, 0) + 1
        
        common_interventions = sorted(
            intervention_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:3]
        
        return {
            "most_impactful_interventions": [{"intervention": interv, "frequency": count} for interv, count in common_interventions],
            "decision_sensitivity": branch_set.variance_analysis.get("volatility_score", 0.5),
            "intervention_timing": "immediate" if any(b.overall_risk_score > 0.7 for b in branches) else "planned"
        }