"""
StadiumVerse AI V2 - AI Storyteller Engine
Transforms technical data and predictions into natural language narratives
"""

import logging
from typing import Dict, List, Any
from enum import Enum

from ..providers.factory import get_global_ai_provider
from ..debate.debate_models import DebateSession
from ..collective_intelligence.impact_models import InterventionProposal

logger = logging.getLogger(__name__)


class NarrativeStyle(str, Enum):
    """Different storytelling styles available"""

    PROFESSIONAL = "professional"  # For FIFA officials and management
    CASUAL = "casual"  # For general staff and volunteers
    TECHNICAL = "technical"  # For technical staff and analysts
    BROADCAST = "broadcast"  # Stadium announcements
    EMERGENCY = "emergency"  # Emergency communications
    EDUCATIONAL = "educational"  # Training and explanation


class StorytellerEngine:
    """
    AI-powered storyteller that converts data into compelling narratives
    """

    def __init__(self):
        self.narrative_cache = {}
        self.story_templates = self._initialize_story_templates()
        self.performance_metrics = {
            "stories_generated": 0,
            "avg_generation_time": 0.0,
            "cache_hits": 0,
            "narrative_accuracy": 0.85,
        }

        logger.info("AI Storyteller Engine initialized")

    def _initialize_story_templates(self) -> Dict[str, Dict[str, str]]:
        """Initialize narrative templates for different scenarios"""
        return {
            "crowd_prediction": {
                NarrativeStyle.PROFESSIONAL: """
Based on current analysis, we anticipate {fan_count} fans will move toward {location} within {timeframe}. 
Current projections indicate {impact_description}. 
Recommended action: {recommendation} to optimize flow and maintain safety standards.
Confidence level: {confidence}%
""",
                NarrativeStyle.CASUAL: """
Heads up team - we're expecting about {fan_count} fans heading to {location} in the next {timeframe}. 
{impact_description}
Here's what we should do: {recommendation}
We're {confidence}% confident this will work well.
""",
                NarrativeStyle.BROADCAST: """
Attention stadium guests: To ensure your comfort and safety, we recommend {recommendation}. 
Current wait times at {location} are approximately {wait_time} minutes. 
Thank you for your cooperation.
""",
            },
            "intervention_explanation": {
                NarrativeStyle.PROFESSIONAL: """
Intervention Analysis: {intervention_title}

Situation: {current_situation}
Recommended Action: {intervention_description}
Expected Impact: {impact_summary}
Implementation: {implementation_steps}
Resource Requirements: {resource_summary}
ROI Assessment: {roi_summary}
Risk Level: {risk_level}

This intervention addresses {problem_statement} and is projected to {benefit_statement}.
Timeline: {implementation_timeline}
Success Probability: {success_probability}%
""",
                NarrativeStyle.CASUAL: """
Quick Update: {intervention_title}

What's happening: {current_situation}
What we're doing: {intervention_description}
Why this helps: {benefit_statement}
What we need: {resource_summary}
How long: {implementation_timeline}

This should {impact_summary} and we're {success_probability}% confident it'll work.
""",
                NarrativeStyle.TECHNICAL: """
Technical Brief: {intervention_title}

Current Metrics: {current_metrics}
Target Metrics: {target_metrics}
Implementation Vector: {intervention_description}
Resource Allocation: {resource_details}
Performance Indicators: {success_metrics}
Fallback Protocols: {fallback_plan}
Confidence Interval: {confidence_range}%

Expected ROI: {roi_details}
Risk Factors: {risk_factors}
""",
            },
            "debate_summary": {
                NarrativeStyle.PROFESSIONAL: """
AI Debate Summary: {topic}

Trigger: {trigger_event}
Participants: {agent_count} AI agents
Duration: {debate_duration}

Consensus Reached: {consensus_level}% agreement
Final Decision: {final_decision}
Implementation: {implementation_plan}
Resource Impact: {resource_impact}

Key Considerations:
{agent_highlights}

Decision Quality Score: {decision_quality}/100
Recommended Action: {final_recommendation}
""",
                NarrativeStyle.CASUAL: """
AI Team Decision: {topic}

The AI agents just finished discussing {trigger_event}.
After {debate_duration} of analysis, they reached {consensus_level}% agreement.

Decision: {final_decision}
Next steps: {implementation_plan}
Confidence: {confidence_level}%

{key_insights}
""",
            },
            "future_scenario": {
                NarrativeStyle.PROFESSIONAL: """
Scenario Analysis: {scenario_timeframe}

Current Trajectory: {current_path}
Projected Outcome: {projected_outcome}

Best Case: {best_case_description}
Expected Case: {likely_case_description}  
Worst Case: {worst_case_description}

Critical Decision Points: {decision_points}
Recommended Monitoring: {monitoring_priorities}
Contingency Triggers: {contingency_conditions}
""",
                NarrativeStyle.BROADCAST: """
Stadium Update:

Current conditions are {current_conditions}. 
{time_reference}, we expect {expected_conditions}.
{public_recommendation}

Thank you for your patience and cooperation.
""",
            },
        }

    async def generate_crowd_narrative(
        self,
        crowd_data: Dict[str, Any],
        prediction_data: Dict[str, Any],
        style: NarrativeStyle = NarrativeStyle.PROFESSIONAL,
        include_recommendations: bool = True,
    ) -> str:
        """Generate narrative for crowd movement and density predictions"""

        try:
            # Extract key information
            fan_count = crowd_data.get("total_fans", "several hundred")
            location = prediction_data.get("target_location", "key stadium areas")
            timeframe = prediction_data.get("timeframe", "the next 15 minutes")
            confidence = prediction_data.get("confidence", 75)
            wait_time = crowd_data.get("avg_wait_time", 8)

            # Determine impact description
            stress_level = crowd_data.get("avg_stress_level", 50)
            if stress_level > 70:
                impact_desc = "elevated stress levels and potential congestion"
            elif stress_level < 30:
                impact_desc = "smooth flow and positive fan experience"
            else:
                impact_desc = "manageable conditions with standard protocols"

            # Generate recommendation
            recommendation = await self._generate_smart_recommendation(
                crowd_data, prediction_data
            )

            # Use template or generate custom narrative
            if (
                "crowd_prediction" in self.story_templates
                and style in self.story_templates["crowd_prediction"]
            ):
                template = self.story_templates["crowd_prediction"][style]
                narrative = template.format(
                    fan_count=fan_count,
                    location=location,
                    timeframe=timeframe,
                    impact_description=impact_desc,
                    recommendation=recommendation,
                    confidence=confidence,
                    wait_time=wait_time,
                )
            else:
                # Generate custom narrative using AI
                narrative = await self._generate_custom_narrative(
                    "crowd_prediction",
                    {
                        "crowd_data": crowd_data,
                        "prediction_data": prediction_data,
                        "style": style.value,
                    },
                )

            self.performance_metrics["stories_generated"] += 1
            return narrative.strip()

        except Exception as e:
            logger.error(f"Error generating crowd narrative: {e}")
            return f"Crowd analysis indicates {fan_count} fans moving toward {location} in {timeframe}. Monitoring situation closely."

    async def generate_intervention_story(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any],
        style: NarrativeStyle = NarrativeStyle.PROFESSIONAL,
    ) -> str:
        """Generate compelling narrative for intervention proposals"""

        try:
            # Extract intervention details
            intervention_data = {
                "intervention_title": proposal.title,
                "intervention_description": proposal.description,
                "current_situation": self._describe_current_situation(current_state),
                "impact_summary": self._summarize_impacts(proposal.impact_assessments),
                "implementation_steps": "; ".join(proposal.implementation_steps[:3]),
                "resource_summary": self._summarize_resources(
                    proposal.resource_requirements
                ),
                "roi_summary": self._summarize_roi(proposal.roi_analysis)
                if proposal.roi_analysis
                else "Cost-benefit analysis pending",
                "risk_level": self._describe_risk_level(proposal.urgency_score),
                "problem_statement": self._generate_problem_statement(
                    proposal, current_state
                ),
                "benefit_statement": self._generate_benefit_statement(proposal),
                "implementation_timeline": f"{proposal.estimated_implementation_time} minutes",
                "success_probability": int(proposal.success_probability * 100),
            }

            # Add technical details if needed
            if style == NarrativeStyle.TECHNICAL:
                intervention_data.update(
                    {
                        "current_metrics": self._format_current_metrics(current_state),
                        "target_metrics": self._format_target_metrics(proposal),
                        "resource_details": self._format_resource_details(proposal),
                        "success_metrics": self._format_success_metrics(proposal),
                        "fallback_plan": proposal.alternative_options[0]
                        if proposal.alternative_options
                        else "Manual override available",
                        "confidence_range": f"{max(50, int((proposal.success_probability - 0.1) * 100))}-{min(95, int((proposal.success_probability + 0.1) * 100))}",
                        "roi_details": self._format_roi_details(proposal.roi_analysis)
                        if proposal.roi_analysis
                        else "ROI calculation in progress",
                        "risk_factors": "; ".join(proposal.alternative_options[:2]),
                    }
                )

            # Generate narrative using template or AI
            template_key = "intervention_explanation"
            if (
                template_key in self.story_templates
                and style in self.story_templates[template_key]
            ):
                template = self.story_templates[template_key][style]
                narrative = template.format(**intervention_data)
            else:
                narrative = await self._generate_custom_narrative(
                    template_key,
                    {"proposal_data": intervention_data, "style": style.value},
                )

            return narrative.strip()

        except Exception as e:
            logger.error(f"Error generating intervention story: {e}")
            return f"Intervention '{proposal.title}' recommended to address current stadium conditions. Implementation time: {proposal.estimated_implementation_time} minutes."

    async def generate_debate_story(
        self,
        debate_session: DebateSession,
        style: NarrativeStyle = NarrativeStyle.PROFESSIONAL,
        include_agent_details: bool = True,
    ) -> str:
        """Generate narrative summary of AI debate session"""

        try:
            # Calculate debate duration in human-readable format
            duration = debate_session.total_duration_seconds
            if duration < 60:
                duration_str = f"{int(duration)} seconds"
            elif duration < 3600:
                duration_str = f"{int(duration / 60)} minutes"
            else:
                duration_str = f"{int(duration / 3600)} hours {int((duration % 3600) / 60)} minutes"

            # Generate agent highlights
            agent_highlights = []
            if include_agent_details and debate_session.agent_positions:
                high_confidence_positions = [
                    pos
                    for pos in debate_session.agent_positions
                    if pos.confidence > 0.8
                ]
                for pos in high_confidence_positions[:3]:  # Top 3 most confident
                    highlight = f"• {pos.agent_name.value.title()}: {pos.recommendation} ({int(pos.confidence * 100)}% confidence)"
                    agent_highlights.append(highlight)

            debate_data = {
                "topic": debate_session.topic,
                "trigger_event": debate_session.trigger_event,
                "agent_count": len(debate_session.agent_positions),
                "debate_duration": duration_str,
                "consensus_level": int(debate_session.get_consensus_score() * 100),
                "final_decision": debate_session.final_decision.decision
                if debate_session.final_decision
                else "No decision reached",
                "implementation_plan": "; ".join(
                    debate_session.final_decision.implementation_steps[:3]
                )
                if debate_session.final_decision
                and debate_session.final_decision.implementation_steps
                else "Implementation pending",
                "resource_impact": f"${debate_session.final_decision.roi_analysis.get('total_cost', 0):.0f}"
                if debate_session.final_decision
                and debate_session.final_decision.roi_analysis
                else "Cost analysis pending",
                "agent_highlights": "\n".join(agent_highlights)
                if agent_highlights
                else "All agents participated in consensus building",
                "decision_quality": int(
                    debate_session.final_decision.get_decision_quality_score() * 100
                )
                if debate_session.final_decision
                else 0,
                "final_recommendation": debate_session.final_decision.decision
                if debate_session.final_decision
                else "Further analysis required",
                "confidence_level": int(debate_session.final_decision.confidence * 100)
                if debate_session.final_decision
                else 0,
                "key_insights": self._extract_debate_insights(debate_session),
            }

            # Generate narrative
            template_key = "debate_summary"
            if (
                template_key in self.story_templates
                and style in self.story_templates[template_key]
            ):
                template = self.story_templates[template_key][style]
                narrative = template.format(**debate_data)
            else:
                narrative = await self._generate_custom_narrative(
                    template_key, {"debate_data": debate_data, "style": style.value}
                )

            return narrative.strip()

        except Exception as e:
            logger.error(f"Error generating debate story: {e}")
            return f"AI debate on '{debate_session.topic}' concluded with {len(debate_session.agent_positions)} agents participating. Decision: {debate_session.final_decision.decision if debate_session.final_decision else 'Pending'}."

    async def generate_future_scenario_story(
        self,
        scenario_data: Dict[str, Any],
        style: NarrativeStyle = NarrativeStyle.PROFESSIONAL,
        timeframe: str = "next 30 minutes",
    ) -> str:
        """Generate narrative for future scenario predictions"""

        try:
            # Process scenario branches
            branches = scenario_data.get("branches", {})
            best_case = branches.get("best_case", {})
            likely_case = branches.get("most_likely", {})
            worst_case = branches.get("worst_case", {})

            scenario_narrative_data = {
                "scenario_timeframe": timeframe,
                "current_path": scenario_data.get(
                    "current_trajectory", "Standard operational trajectory"
                ),
                "projected_outcome": likely_case.get(
                    "description", "Expected operational outcome"
                ),
                "best_case_description": best_case.get(
                    "description", "Optimal conditions achieved"
                ),
                "likely_case_description": likely_case.get(
                    "description", "Standard conditions maintained"
                ),
                "worst_case_description": worst_case.get(
                    "description", "Challenging conditions managed"
                ),
                "decision_points": self._identify_decision_points(scenario_data),
                "monitoring_priorities": self._identify_monitoring_priorities(
                    scenario_data
                ),
                "contingency_conditions": self._identify_contingency_triggers(
                    scenario_data
                ),
                "current_conditions": scenario_data.get(
                    "current_conditions", "normal operations"
                ),
                "time_reference": f"Over the {timeframe}",
                "expected_conditions": likely_case.get(
                    "summary", "standard service levels"
                ),
                "public_recommendation": self._generate_public_recommendation(
                    scenario_data
                ),
            }

            # Generate narrative
            template_key = "future_scenario"
            if (
                template_key in self.story_templates
                and style in self.story_templates[template_key]
            ):
                template = self.story_templates[template_key][style]
                narrative = template.format(**scenario_narrative_data)
            else:
                narrative = await self._generate_custom_narrative(
                    template_key,
                    {"scenario_data": scenario_narrative_data, "style": style.value},
                )

            return narrative.strip()

        except Exception as e:
            logger.error(f"Error generating scenario story: {e}")
            return f"Future scenario analysis for {timeframe} indicates {scenario_data.get('summary', 'continued operational focus')}."

    async def _generate_custom_narrative(
        self, narrative_type: str, context_data: Dict[str, Any]
    ) -> str:
        """Generate custom narrative using AI when templates aren't sufficient"""

        ai_provider = await get_global_ai_provider()

        f"""
Generate a compelling narrative for {narrative_type} with the following data:

{context_data}

Create a narrative that:
1. Explains the situation clearly and concisely
2. Uses specific numbers and timeframes when available
3. Maintains professional but engaging tone
4. Focuses on actionable insights
5. Includes clear recommendations
6. Uses natural, flowing language

Style: {context_data.get("style", "professional")}

Keep the narrative focused, informative, and engaging. Use active voice and concrete details.
"""

        try:
            response = await ai_provider.generate_storyteller_response(
                scenario=context_data, style=context_data.get("style", "professional")
            )

            return response.content

        except Exception as e:
            logger.error(f"Error generating custom narrative: {e}")
            return "Analysis indicates ongoing stadium operations require continued monitoring and standard protocols."

    async def _generate_smart_recommendation(
        self, crowd_data: Dict[str, Any], prediction_data: Dict[str, Any]
    ) -> str:
        """Generate intelligent recommendations based on crowd and prediction data"""

        stress_level = crowd_data.get("avg_stress_level", 50)
        queue_time = crowd_data.get("avg_queue_time", 10)
        fan_count = crowd_data.get("total_fans", 1000)

        if stress_level > 80 or queue_time > 20:
            return "deploy additional volunteers and open secondary pathways"
        elif stress_level > 60 or queue_time > 15:
            return "increase communication and monitor closely"
        elif fan_count > 5000:
            return "prepare for increased capacity and ensure adequate staffing"
        else:
            return "maintain standard protocols with ongoing monitoring"

    def _describe_current_situation(self, current_state: Dict[str, Any]) -> str:
        """Create human-readable description of current stadium state"""

        total_fans = current_state.get("total_fans", "Unknown")
        stress_level = current_state.get("avg_stress_level", 50)

        if stress_level > 70:
            condition = "elevated activity levels with increased crowd density"
        elif stress_level < 30:
            condition = "calm conditions with normal operations"
        else:
            condition = "standard operational conditions"

        return f"Stadium currently hosts {total_fans} fans with {condition}"

    def _summarize_impacts(self, impact_assessments: List) -> str:
        """Summarize impact assessments in natural language"""
        if not impact_assessments:
            return "Impact assessment in progress"

        impact_summaries = []
        for assessment in impact_assessments[:3]:  # Top 3 impacts
            magnitude = abs(
                assessment.predicted_improvement - assessment.current_baseline
            )
            if magnitude > 20:
                level = "significant"
            elif magnitude > 10:
                level = "moderate"
            else:
                level = "minor"

            impact_summaries.append(
                f"{level} {assessment.category.value.replace('_', ' ')}"
            )

        return " and ".join(impact_summaries)

    def _summarize_resources(self, resource_requirements: List[str]) -> str:
        """Summarize resource requirements"""
        if not resource_requirements:
            return "minimal resources required"

        if len(resource_requirements) == 1:
            return resource_requirements[0].lower()
        elif len(resource_requirements) <= 3:
            return " and ".join(resource_requirements).lower()
        else:
            return f"{len(resource_requirements)} operational resources including {resource_requirements[0].lower()}"

    def _summarize_roi(self, roi_analysis) -> str:
        """Summarize ROI analysis"""
        if not roi_analysis:
            return "ROI analysis pending"

        roi_ratio = roi_analysis.roi_ratio
        if roi_ratio >= 2.0:
            return f"excellent ROI ({roi_ratio:.1f}:1 benefit-to-cost ratio)"
        elif roi_ratio >= 1.5:
            return f"strong ROI ({roi_ratio:.1f}:1 benefit-to-cost ratio)"
        elif roi_ratio >= 1.0:
            return f"positive ROI ({roi_ratio:.1f}:1 benefit-to-cost ratio)"
        else:
            return "cost-benefit analysis indicates operational focus needed"

    def _describe_risk_level(self, urgency_score: float) -> str:
        """Convert urgency score to risk level description"""
        if urgency_score >= 0.8:
            return "High - immediate action required"
        elif urgency_score >= 0.6:
            return "Medium - timely action recommended"
        elif urgency_score >= 0.4:
            return "Low - standard protocols sufficient"
        else:
            return "Minimal - monitoring and preparation"

    def _generate_problem_statement(
        self, proposal, current_state: Dict[str, Any]
    ) -> str:
        """Generate clear problem statement"""
        intervention_mapping = {
            "volunteer_deployment": "insufficient staffing in high-traffic areas",
            "gate_operation": "crowd flow bottlenecks at entry/exit points",
            "queue_management": "extended wait times impacting fan experience",
            "communication": "information gaps causing confusion",
            "resource_allocation": "suboptimal resource distribution",
            "transport_adjustment": "transportation coordination challenges",
            "facility_operation": "facility capacity limitations",
            "emergency_preparation": "potential safety and security concerns",
        }

        return intervention_mapping.get(
            proposal.intervention_type.value, "operational optimization opportunities"
        )

    def _generate_benefit_statement(self, proposal) -> str:
        """Generate clear benefit statement"""
        if not proposal.impact_assessments:
            return "improve overall operational efficiency"

        primary_impact = proposal.impact_assessments[0]
        impact_type = primary_impact.category.value.replace("_", " ")

        return f"enhance {impact_type} by approximately {abs(primary_impact.predicted_improvement - primary_impact.current_baseline):.1f}%"

    # Additional helper methods for formatting technical details
    def _format_current_metrics(self, current_state: Dict[str, Any]) -> str:
        """Format current metrics for technical narrative"""
        metrics = []
        key_metrics = [
            "total_fans",
            "avg_stress_level",
            "avg_queue_time",
            "operational_efficiency",
        ]

        for metric in key_metrics:
            if metric in current_state:
                metrics.append(f"{metric.replace('_', ' ')}: {current_state[metric]}")

        return "; ".join(metrics) if metrics else "Standard operational metrics"

    def _format_target_metrics(self, proposal) -> str:
        """Format target metrics after intervention"""
        if not proposal.impact_assessments:
            return "Target metrics calculation in progress"

        targets = []
        for assessment in proposal.impact_assessments[:3]:
            target = f"{assessment.category.value.replace('_', ' ')}: {assessment.predicted_improvement:.1f}"
            targets.append(target)

        return "; ".join(targets)

    def _extract_debate_insights(self, debate_session: DebateSession) -> str:
        """Extract key insights from debate session"""
        insights = []

        if debate_session.agent_positions:
            # Find highest confidence position
            highest_conf = max(
                debate_session.agent_positions, key=lambda p: p.confidence
            )
            insights.append(
                f"{highest_conf.agent_name.value.title()} agent showed highest confidence ({highest_conf.confidence:.0%})"
            )

            # Check for risk concerns
            risk_concerns = [
                p
                for p in debate_session.agent_positions
                if p.risk_assessment in ["high", "critical"]
            ]
            if risk_concerns:
                insights.append(
                    f"{len(risk_concerns)} agents identified elevated risk factors"
                )

            # Check for consensus
            consensus = debate_session.get_consensus_score()
            if consensus > 0.8:
                insights.append("Strong consensus achieved across all agents")
            elif consensus < 0.5:
                insights.append("Diverse perspectives required additional analysis")

        return ". ".join(insights) if insights else "Comprehensive analysis completed"

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get storyteller performance metrics"""
        return self.performance_metrics.copy()

    def clear_narrative_cache(self):
        """Clear narrative cache to free memory"""
        self.narrative_cache.clear()
        logger.info("Narrative cache cleared")

    # Helper methods for scenario narratives
    def _identify_decision_points(self, scenario_data: Dict[str, Any]) -> str:
        """Identify critical decision points in scenarios"""
        return "Gate operations, volunteer deployment, and communication timing"

    def _identify_monitoring_priorities(self, scenario_data: Dict[str, Any]) -> str:
        """Identify what should be monitored"""
        return "Crowd density, queue lengths, and fan satisfaction levels"

    def _identify_contingency_triggers(self, scenario_data: Dict[str, Any]) -> str:
        """Identify contingency activation triggers"""
        return "Stress levels exceeding 80%, queue times over 20 minutes, or emergency situations"

    def _generate_public_recommendation(self, scenario_data: Dict[str, Any]) -> str:
        """Generate public-facing recommendation"""
        return "Please follow stadium signage and volunteer guidance for the best experience"
