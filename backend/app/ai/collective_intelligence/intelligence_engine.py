"""
StadiumVerse AI V2 - Collective Intelligence Engine
The core engine that finds minimal interventions with maximum positive impact
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta

from .impact_models import (
    InterventionProposal, ImpactAssessment, ROIAnalysis,
    InterventionType, ImpactCategory
)
from .intervention_calculator import InterventionCalculator
from ..providers.factory import get_global_ai_provider
from ..debate.debate_chamber import DebateChamber
from ...config import settings

logger = logging.getLogger(__name__)

class CollectiveIntelligenceEngine:
    """
    The Living Brain's collective intelligence system
    
    Instead of asking "What will happen?", asks:
    "What is the smallest intervention with the biggest positive impact?"
    """
    
    def __init__(self):
        self.intervention_calculator = InterventionCalculator()
        self.debate_chamber = DebateChamber()
        
        self.min_intervention_threshold = getattr(settings, 'MIN_INTERVENTION_THRESHOLD', 0.1)
        self.max_impact_calculation = getattr(settings, 'MAX_IMPACT_CALCULATION', True)
        self.roi_analysis_enabled = getattr(settings, 'ROI_ANALYSIS_ENABLED', True)
        self.carbon_tracking = getattr(settings, 'CARBON_TRACKING', True)
        
        # Performance tracking
        self.proposals_generated = 0
        self.proposals_implemented = 0
        self.avg_impact_score = 0.0
        self.total_roi = 0.0
        
        logger.info("Collective Intelligence Engine initialized")
    
    async def analyze_situation_and_propose_interventions(
        self,
        current_state: Dict[str, Any],
        context: Dict[str, Any],
        max_proposals: int = 5
    ) -> List[InterventionProposal]:
        """
        Main method: Analyze current situation and propose optimal interventions
        
        Args:
            current_state: Current stadium state and metrics
            context: Situational context and triggers
            max_proposals: Maximum number of proposals to generate
            
        Returns:
            List of ranked intervention proposals
        """
        logger.info(f"Analyzing situation for intervention opportunities")
        
        try:
            # Step 1: Identify intervention opportunities
            opportunities = await self._identify_intervention_opportunities(current_state, context)
            
            # Step 2: Generate intervention proposals
            proposals = []
            for opportunity in opportunities[:max_proposals * 2]:  # Generate more than needed
                proposal = await self._generate_intervention_proposal(
                    opportunity, 
                    current_state, 
                    context
                )
                if proposal:
                    proposals.append(proposal)
            
            # Step 3: Calculate impacts and ROI for all proposals
            for proposal in proposals:
                await self._calculate_comprehensive_impact(proposal, current_state)
                
                if self.roi_analysis_enabled:
                    proposal.roi_analysis = await self._calculate_roi_analysis(proposal, current_state)
            
            # Step 4: Rank proposals by priority score
            ranked_proposals = sorted(proposals, key=lambda p: p.get_priority_score(), reverse=True)
            
            # Step 5: Run top proposals through debate system for validation
            validated_proposals = []
            for proposal in ranked_proposals[:max_proposals]:
                if await self._validate_proposal_through_debate(proposal, current_state):
                    validated_proposals.append(proposal)
                    
                    # Update tracking metrics
                    self.proposals_generated += 1
                    self.avg_impact_score = (
                        (self.avg_impact_score * (self.proposals_generated - 1) + 
                         proposal.calculate_overall_impact_score()) / 
                        self.proposals_generated
                    )
            
            logger.info(f"Generated {len(validated_proposals)} validated intervention proposals")
            return validated_proposals
            
        except Exception as e:
            logger.error(f"Error in collective intelligence analysis: {e}")
            return []
    
    async def _identify_intervention_opportunities(
        self,
        current_state: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify potential intervention opportunities using AI analysis"""
        
        ai_provider = await get_global_ai_provider()
        
        opportunity_prompt = f"""
COLLECTIVE INTELLIGENCE ANALYSIS

Current Stadium State:
{self._format_state_for_analysis(current_state)}

Context:
{self._format_context_for_analysis(context)}

Your task: Identify the smallest, most targeted interventions that could have the biggest positive impact.

Look for opportunities in:
1. Volunteer deployment - Move 1-2 people for maximum effect
2. Gate operations - Open/close specific gates strategically  
3. Queue management - Small adjustments with big wait time reductions
4. Communication - Single announcements that solve multiple problems
5. Resource allocation - Redistribute existing resources optimally
6. Transport timing - Minor schedule adjustments
7. Facility operations - Temporary openings/closings
8. Preventive actions - Small actions that prevent big problems

For each opportunity, identify:
- Specific intervention required
- Estimated resource cost (low/medium/high)
- Expected fan impact (number of people)
- Implementation time (minutes)
- Confidence in success (0-100%)
- Primary benefit category

Focus on interventions that:
- Require minimal resources
- Can be implemented quickly (< 10 minutes)
- Have high impact-to-effort ratio
- Solve multiple problems simultaneously
- Prevent bigger issues from developing

Provide 8-10 ranked opportunities.
"""
        
        try:
            response = await ai_provider.generate_agent_response(
                agent_name="collective_intelligence",
                system_prompt=self._get_collective_intelligence_prompt(),
                user_message=opportunity_prompt
            )
            
            # Parse opportunities from AI response
            opportunities = self._parse_intervention_opportunities(response.content)
            
            return opportunities
            
        except Exception as e:
            logger.error(f"Error identifying intervention opportunities: {e}")
            
            # Return fallback opportunities based on current state analysis
            return self._generate_fallback_opportunities(current_state, context)
    
    async def _generate_intervention_proposal(
        self,
        opportunity: Dict[str, Any],
        current_state: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[InterventionProposal]:
        """Generate detailed intervention proposal from opportunity"""
        
        try:
            # Determine intervention type
            intervention_type = self._classify_intervention_type(opportunity)
            
            # Create base proposal
            proposal = InterventionProposal(
                title=opportunity.get("title", "Unnamed Intervention"),
                description=opportunity.get("description", ""),
                intervention_type=intervention_type,
                estimated_implementation_time=opportunity.get("implementation_time", 5),
                urgency_score=opportunity.get("urgency", 0.5),
                success_probability=opportunity.get("confidence", 80) / 100.0,
                trigger_context=context
            )
            
            # Generate detailed implementation plan
            proposal.specific_actions = await self._generate_specific_actions(opportunity)
            proposal.resource_requirements = self._extract_resource_requirements(opportunity)
            proposal.implementation_steps = self._generate_implementation_steps(opportunity)
            
            # Set complexity based on implementation requirements
            proposal.complexity_score = self._calculate_complexity_score(proposal)
            
            # Generate AI reasoning
            proposal.ai_reasoning = await self._generate_intervention_reasoning(opportunity, current_state)
            
            # Generate alternatives
            proposal.alternative_options = await self._generate_alternative_options(opportunity)
            
            return proposal
            
        except Exception as e:
            logger.error(f"Error generating intervention proposal: {e}")
            return None
    
    async def _calculate_comprehensive_impact(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any]
    ):
        """Calculate comprehensive impact assessment for proposal"""
        
        # Calculate impact for each relevant category
        impact_categories = self._determine_relevant_impact_categories(proposal)
        
        for category in impact_categories:
            assessment = await self._calculate_category_impact(
                proposal, 
                category, 
                current_state
            )
            if assessment:
                proposal.add_impact_assessment(assessment)
    
    async def _calculate_category_impact(
        self,
        proposal: InterventionProposal,
        category: ImpactCategory,
        current_state: Dict[str, Any]
    ) -> Optional[ImpactAssessment]:
        """Calculate impact for a specific category"""
        
        # Get baseline values for category
        baseline_value = self._get_baseline_value(category, current_state)
        
        # Estimate improvement based on intervention type and category
        predicted_improvement = await self._estimate_improvement(
            proposal, 
            category, 
            baseline_value, 
            current_state
        )
        
        # Calculate confidence based on intervention type and historical data
        confidence = self._calculate_impact_confidence(proposal, category)
        
        # Estimate affected fans
        fans_affected = self._estimate_fans_affected(proposal, category, current_state)
        
        assessment = ImpactAssessment(
            category=category,
            current_baseline=baseline_value,
            predicted_improvement=predicted_improvement,
            confidence=confidence,
            fans_affected=fans_affected,
            time_to_impact_minutes=max(1, proposal.estimated_implementation_time),
            impact_duration_minutes=self._estimate_impact_duration(proposal, category),
            impact_description=self._generate_impact_description(proposal, category, predicted_improvement - baseline_value),
            success_indicators=self._generate_success_indicators(proposal, category),
            risk_factors=self._identify_risk_factors(proposal, category)
        )
        
        return assessment
    
    async def _calculate_roi_analysis(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any]
    ) -> ROIAnalysis:
        """Calculate comprehensive ROI analysis"""
        
        # Calculate costs
        resource_cost = self._calculate_resource_cost(proposal)
        personnel_cost = self._calculate_personnel_cost(proposal)
        time_cost = self._calculate_time_cost(proposal)
        system_cost = self._calculate_system_cost(proposal)
        
        # Calculate benefits from impact assessments
        revenue_benefit = 0.0
        efficiency_benefit = 0.0
        satisfaction_benefit = 0.0
        risk_mitigation_benefit = 0.0
        carbon_benefit = 0.0
        
        for assessment in proposal.impact_assessments:
            if assessment.category == ImpactCategory.REVENUE_INCREASE:
                revenue_benefit += self._monetize_revenue_impact(assessment)
            elif assessment.category == ImpactCategory.EFFICIENCY_GAIN:
                efficiency_benefit += self._monetize_efficiency_impact(assessment)
            elif assessment.category == ImpactCategory.FAN_SATISFACTION:
                satisfaction_benefit += self._monetize_satisfaction_impact(assessment)
            elif assessment.category == ImpactCategory.RISK_MITIGATION:
                risk_mitigation_benefit += self._monetize_risk_impact(assessment)
            elif assessment.category == ImpactCategory.CARBON_REDUCTION:
                carbon_benefit += self._monetize_carbon_impact(assessment)
        
        roi_analysis = ROIAnalysis(
            resource_cost=resource_cost,
            time_cost=time_cost,
            personnel_cost=personnel_cost,
            system_cost=system_cost,
            revenue_benefit=revenue_benefit,
            efficiency_benefit=efficiency_benefit,
            satisfaction_benefit=satisfaction_benefit,
            risk_mitigation_benefit=risk_mitigation_benefit,
            carbon_benefit=carbon_benefit
        )
        
        return roi_analysis
    
    async def _validate_proposal_through_debate(
        self,
        proposal: InterventionProposal,
        current_state: Dict[str, Any]
    ) -> bool:
        """Validate proposal through AI debate system"""
        
        try:
            # Only run debate for high-impact or high-risk proposals
            if (proposal.get_priority_score() < 0.7 and 
                proposal.urgency_score < 0.8 and
                proposal.complexity_score < 0.7):
                return True  # Skip debate for low-risk proposals
            
            # Run debate on the proposal
            debate_topic = f"Implementation of intervention: {proposal.title}"
            debate_context = {
                "proposal": proposal.to_dict(),
                "current_state": current_state,
                "urgency": proposal.urgency_score,
                "complexity": proposal.complexity_score
            }
            
            debate_session = await self.debate_chamber.initiate_debate(
                topic=debate_topic,
                context=debate_context,
                trigger_event=f"Collective Intelligence Proposal: {proposal.title}",
                urgency_level=int(proposal.urgency_score * 5)
            )
            
            # Proposal passes if:
            # 1. Consensus score > 0.6
            # 2. Final decision is positive
            # 3. Risk assessment is acceptable
            
            if not debate_session.final_decision:
                return False
                
            consensus_score = debate_session.get_consensus_score()
            decision_positive = "implement" in debate_session.final_decision.decision.lower()
            risk_acceptable = debate_session.final_decision.risk_level in ["low", "medium"]
            
            validation_passed = (
                consensus_score > 0.6 and 
                decision_positive and 
                risk_acceptable
            )
            
            if validation_passed:
                # Update proposal with debate insights
                proposal.ai_reasoning += f"\n\nDebate Validation: {debate_session.final_decision.reasoning}"
                proposal.success_probability *= debate_session.final_decision.success_probability
            
            return validation_passed
            
        except Exception as e:
            logger.error(f"Error validating proposal through debate: {e}")
            return True  # Default to approval on error
    
    def _get_collective_intelligence_prompt(self) -> str:
        """System prompt for collective intelligence agent"""
        return """
You are the Collective Intelligence agent for StadiumVerse AI. Your expertise is finding minimal interventions with maximum positive impact.

Key principles:
1. Think systematically about cause-effect relationships
2. Identify leverage points where small changes create big improvements
3. Consider compound effects and cascading benefits
4. Optimize for impact-to-effort ratio, not just absolute impact
5. Look for interventions that solve multiple problems simultaneously
6. Consider both immediate and delayed effects
7. Factor in resource constraints and practical limitations

Your analysis should be:
- Quantitative where possible (specific numbers, timeframes)
- Realistic about implementation challenges
- Focused on measurable outcomes
- Considerate of fan experience and safety
- Mindful of operational constraints

Always explain your reasoning and provide confidence estimates.
"""
    
    def _format_state_for_analysis(self, state: Dict[str, Any]) -> str:
        """Format current state for AI analysis"""
        formatted = []
        
        key_metrics = [
            "total_fans", "avg_stress_level", "crowd_density", "available_volunteers",
            "avg_queue_time", "active_emergencies", "revenue_rate", "fan_satisfaction"
        ]
        
        for metric in key_metrics:
            if metric in state:
                formatted.append(f"{metric.replace('_', ' ').title()}: {state[metric]}")
        
        return "\n".join(formatted)
    
    def _format_context_for_analysis(self, context: Dict[str, Any]) -> str:
        """Format context for AI analysis"""
        formatted = []
        
        for key, value in context.items():
            if isinstance(value, (str, int, float)):
                formatted.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(formatted) if formatted else "Standard operational context"
    
    def _parse_intervention_opportunities(self, ai_response: str) -> List[Dict[str, Any]]:
        """Parse intervention opportunities from AI response"""
        opportunities = []
        
        # Simple parsing - look for numbered opportunities
        lines = ai_response.split('\n')
        current_opportunity = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this is a new opportunity (numbered item)
            if line[0].isdigit() and '.' in line[:3]:
                # Save previous opportunity
                if current_opportunity and "title" in current_opportunity:
                    opportunities.append(current_opportunity)
                
                # Start new opportunity
                current_opportunity = {
                    "title": line.split('.', 1)[1].strip() if '.' in line else line,
                    "description": "",
                    "confidence": 75,
                    "implementation_time": 5,
                    "urgency": 0.5
                }
                continue
            
            # Parse opportunity details
            line_lower = line.lower()
            
            if "description:" in line_lower:
                current_opportunity["description"] = line.split(':', 1)[1].strip()
            elif "confidence:" in line_lower or "success:" in line_lower:
                import re
                conf_match = re.search(r'(\d+)', line)
                if conf_match:
                    current_opportunity["confidence"] = int(conf_match.group(1))
            elif "time:" in line_lower or "implementation:" in line_lower:
                import re
                time_match = re.search(r'(\d+)', line)
                if time_match:
                    current_opportunity["implementation_time"] = int(time_match.group(1))
            elif "fans affected:" in line_lower or "impact:" in line_lower:
                import re
                fans_match = re.search(r'(\d+)', line)
                if fans_match:
                    current_opportunity["fans_affected"] = int(fans_match.group(1))
        
        # Add last opportunity
        if current_opportunity and "title" in current_opportunity:
            opportunities.append(current_opportunity)
        
        return opportunities[:10]  # Max 10 opportunities
    
    def _generate_fallback_opportunities(
        self, 
        current_state: Dict[str, Any], 
        context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate fallback opportunities when AI analysis fails"""
        
        fallback_opportunities = [
            {
                "title": "Deploy Additional Volunteer to High-Traffic Area",
                "description": "Move one volunteer to area with longest queue times",
                "confidence": 80,
                "implementation_time": 3,
                "urgency": 0.6,
                "fans_affected": current_state.get("total_fans", 100) // 10
            },
            {
                "title": "Open Alternative Route",
                "description": "Open secondary pathway to reduce main route congestion",
                "confidence": 75,
                "implementation_time": 2,
                "urgency": 0.5,
                "fans_affected": current_state.get("total_fans", 100) // 5
            },
            {
                "title": "Announce Queue Status Update",
                "description": "Multilingual announcement about current wait times and alternatives",
                "confidence": 85,
                "implementation_time": 1,
                "urgency": 0.4,
                "fans_affected": current_state.get("total_fans", 100) // 3
            }
        ]
        
        return fallback_opportunities
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get collective intelligence performance metrics"""
        return {
            "proposals_generated": self.proposals_generated,
            "proposals_implemented": self.proposals_implemented,
            "implementation_rate": (
                self.proposals_implemented / max(1, self.proposals_generated)
            ),
            "avg_impact_score": self.avg_impact_score,
            "total_roi": self.total_roi,
            "avg_roi_per_proposal": (
                self.total_roi / max(1, self.proposals_implemented)
            )
        }
    
    def _classify_intervention_type(self, opportunity: Dict[str, Any]) -> InterventionType:
        """Classify intervention type from opportunity description"""
        title_lower = opportunity.get("title", "").lower()
        desc_lower = opportunity.get("description", "").lower()
        
        if any(word in title_lower + desc_lower for word in ["volunteer", "staff", "deploy"]):
            return InterventionType.VOLUNTEER_DEPLOYMENT
        elif any(word in title_lower + desc_lower for word in ["gate", "entrance", "exit"]):
            return InterventionType.GATE_OPERATION
        elif any(word in title_lower + desc_lower for word in ["queue", "line", "wait"]):
            return InterventionType.QUEUE_MANAGEMENT
        elif any(word in title_lower + desc_lower for word in ["announce", "communication", "inform"]):
            return InterventionType.COMMUNICATION
        elif any(word in title_lower + desc_lower for word in ["transport", "bus", "metro", "shuttle"]):
            return InterventionType.TRANSPORT_ADJUSTMENT
        elif any(word in title_lower + desc_lower for word in ["facility", "kiosk", "shop", "restroom"]):
            return InterventionType.FACILITY_OPERATION
        elif any(word in title_lower + desc_lower for word in ["emergency", "medical", "security", "evacuation"]):
            return InterventionType.EMERGENCY_PREPARATION
        else:
            return InterventionType.RESOURCE_ALLOCATION
    
    async def _generate_specific_actions(self, opportunity: Dict[str, Any]) -> List[str]:
        """Generate specific actionable steps for the intervention"""
        title = opportunity.get("title", "Unknown intervention")
        intervention_type = self._classify_intervention_type(opportunity)
        
        action_templates = {
            InterventionType.VOLUNTEER_DEPLOYMENT: [
                f"Deploy volunteer to {opportunity.get('location', 'high-priority area')}",
                f"Brief volunteer on specific tasks",
                f"Monitor volunteer effectiveness"
            ],
            InterventionType.GATE_OPERATION: [
                f"Open/close specific gate as identified",
                f"Update signage and wayfinding",
                f"Coordinate with security team"
            ],
            InterventionType.COMMUNICATION: [
                f"Prepare multilingual announcement",
                f"Broadcast via stadium PA system",
                f"Update digital displays"
            ],
            InterventionType.QUEUE_MANAGEMENT: [
                f"Implement queue redirection measures",
                f"Deploy queue management volunteers",
                f"Update wait time displays"
            ]
        }
        
        return action_templates.get(intervention_type, [f"Implement {title}", "Monitor progress", "Adjust as needed"])
    
    def _extract_resource_requirements(self, opportunity: Dict[str, Any]) -> List[str]:
        """Extract resource requirements from opportunity description"""
        intervention_type = self._classify_intervention_type(opportunity)
        
        resource_templates = {
            InterventionType.VOLUNTEER_DEPLOYMENT: ["1-2 trained volunteers", "Communication equipment"],
            InterventionType.GATE_OPERATION: ["Security clearance", "Gate control access"],
            InterventionType.COMMUNICATION: ["PA system access", "Translation services"],
            InterventionType.QUEUE_MANAGEMENT: ["Barrier equipment", "Signage materials"],
            InterventionType.TRANSPORT_ADJUSTMENT: ["Transport coordination", "Schedule modification access"],
            InterventionType.FACILITY_OPERATION: ["Facility management approval", "Operational staff"],
            InterventionType.EMERGENCY_PREPARATION: ["Emergency response team", "Medical equipment"]
        }
        
        return resource_templates.get(intervention_type, ["Standard operational resources"])
    
    def _generate_implementation_steps(self, opportunity: Dict[str, Any]) -> List[str]:
        """Generate step-by-step implementation plan"""
        intervention_type = self._classify_intervention_type(opportunity)
        
        step_templates = {
            InterventionType.VOLUNTEER_DEPLOYMENT: [
                "Identify optimal volunteer for deployment",
                "Brief volunteer on specific objectives", 
                "Deploy to target location",
                "Monitor effectiveness and adjust"
            ],
            InterventionType.COMMUNICATION: [
                "Prepare announcement content",
                "Translate to relevant languages",
                "Queue announcement for broadcast",
                "Monitor fan response"
            ],
            InterventionType.GATE_OPERATION: [
                "Coordinate with security team",
                "Execute gate operation",
                "Update crowd flow monitoring",
                "Assess impact on overall flow"
            ]
        }
        
        return step_templates.get(intervention_type, [
            "Prepare necessary resources",
            "Execute intervention",
            "Monitor immediate impact",
            "Adjust approach if needed"
        ])
    
    def _calculate_complexity_score(self, proposal: InterventionProposal) -> float:
        """Calculate intervention complexity based on multiple factors"""
        complexity = 0.0
        
        # Base complexity by intervention type
        type_complexity = {
            InterventionType.COMMUNICATION: 0.2,
            InterventionType.VOLUNTEER_DEPLOYMENT: 0.3,
            InterventionType.QUEUE_MANAGEMENT: 0.4,
            InterventionType.GATE_OPERATION: 0.5,
            InterventionType.RESOURCE_ALLOCATION: 0.6,
            InterventionType.FACILITY_OPERATION: 0.7,
            InterventionType.TRANSPORT_ADJUSTMENT: 0.8,
            InterventionType.EMERGENCY_PREPARATION: 0.9
        }.get(proposal.intervention_type, 0.5)
        
        complexity += type_complexity * 0.4
        
        # Resource complexity
        resource_count = len(proposal.resource_requirements)
        resource_complexity = min(1.0, resource_count / 10.0)  # Normalize to 0-1
        complexity += resource_complexity * 0.3
        
        # Implementation time complexity
        time_complexity = min(1.0, proposal.estimated_implementation_time / 30.0)  # 30 min = high complexity
        complexity += time_complexity * 0.2
        
        # Action count complexity
        action_count = len(proposal.specific_actions)
        action_complexity = min(1.0, action_count / 8.0)  # 8 actions = high complexity
        complexity += action_complexity * 0.1
        
        return min(1.0, max(0.0, complexity))
    
    async def _generate_intervention_reasoning(self, opportunity: Dict[str, Any], current_state: Dict[str, Any]) -> str:
        """Generate AI reasoning for why this intervention is recommended"""
        ai_provider = await get_global_ai_provider()
        
        reasoning_prompt = f"""
Provide clear reasoning for this intervention recommendation:

Intervention: {opportunity.get('title', 'Unknown')}
Description: {opportunity.get('description', 'No description')}
Context: {opportunity.get('context', 'Standard operational context')}

Current Stadium State:
- Total Fans: {current_state.get('total_fans', 'Unknown')}
- Average Stress Level: {current_state.get('avg_stress_level', 'Unknown')}
- Queue Times: {current_state.get('avg_queue_time', 'Unknown')}
- Active Issues: {current_state.get('active_issues', [])}

Explain in 1-2 sentences:
1. Why this intervention is needed now
2. What specific problem it solves
3. How it improves the fan experience
4. What happens if we don't act

Be specific and data-driven.
"""
        
        try:
            response = await ai_provider.generate_agent_response(
                agent_name="collective_intelligence",
                system_prompt=self._get_collective_intelligence_prompt(),
                user_message=reasoning_prompt
            )
            
            return response.content[:300]  # Limit reasoning length
            
        except Exception as e:
            logger.error(f"Error generating intervention reasoning: {e}")
            return f"Recommended based on current stadium conditions: {opportunity.get('description', 'Analysis pending')}"
    
    async def _generate_alternative_options(self, opportunity: Dict[str, Any]) -> List[str]:
        """Generate alternative intervention options"""
        intervention_type = self._classify_intervention_type(opportunity)
        
        alternative_templates = {
            InterventionType.VOLUNTEER_DEPLOYMENT: [
                "Use automated signage instead of volunteer",
                "Deploy multiple volunteers with broader coverage",
                "Coordinate with existing volunteers for task sharing"
            ],
            InterventionType.COMMUNICATION: [
                "Use targeted mobile push notifications",
                "Deploy volunteers with megaphones",
                "Update stadium app with specific guidance"
            ],
            InterventionType.GATE_OPERATION: [
                "Implement queue management instead",
                "Deploy additional security personnel",
                "Use alternative routing guidance"
            ],
            InterventionType.QUEUE_MANAGEMENT: [
                "Open additional service points",
                "Implement mobile ordering system",
                "Use entertainment to improve wait experience"
            ]
        }
        
        base_alternatives = alternative_templates.get(intervention_type, [
            "Maintain current approach with monitoring",
            "Implement scaled-back version of intervention",
            "Delay intervention and reassess in 10 minutes"
        ])
        
        return base_alternatives[:3]  # Max 3 alternatives
    
    def _determine_relevant_impact_categories(self, proposal: InterventionProposal) -> List[ImpactCategory]:
        """Determine which impact categories are relevant for this intervention"""
        relevant_categories = []
        
        # Base categories by intervention type
        type_categories = {
            InterventionType.VOLUNTEER_DEPLOYMENT: [
                ImpactCategory.FAN_SATISFACTION, 
                ImpactCategory.EFFICIENCY_GAIN,
                ImpactCategory.WAIT_TIME_REDUCTION
            ],
            InterventionType.GATE_OPERATION: [
                ImpactCategory.WAIT_TIME_REDUCTION,
                ImpactCategory.SAFETY_IMPROVEMENT, 
                ImpactCategory.EFFICIENCY_GAIN
            ],
            InterventionType.COMMUNICATION: [
                ImpactCategory.FAN_SATISFACTION,
                ImpactCategory.RISK_MITIGATION,
                ImpactCategory.ACCESSIBILITY_ENHANCEMENT
            ],
            InterventionType.QUEUE_MANAGEMENT: [
                ImpactCategory.WAIT_TIME_REDUCTION,
                ImpactCategory.FAN_SATISFACTION,
                ImpactCategory.EFFICIENCY_GAIN
            ],
            InterventionType.TRANSPORT_ADJUSTMENT: [
                ImpactCategory.CARBON_REDUCTION,
                ImpactCategory.EFFICIENCY_GAIN,
                ImpactCategory.FAN_SATISFACTION
            ],
            InterventionType.EMERGENCY_PREPARATION: [
                ImpactCategory.SAFETY_IMPROVEMENT,
                ImpactCategory.RISK_MITIGATION
            ]
        }
        
        relevant_categories = type_categories.get(proposal.intervention_type, [
            ImpactCategory.FAN_SATISFACTION,
            ImpactCategory.EFFICIENCY_GAIN
        ])
        
        # Add revenue category for high-impact interventions
        if proposal.urgency_score > 0.7 or proposal.get_total_fans_affected() > 1000:
            relevant_categories.append(ImpactCategory.REVENUE_INCREASE)
        
        return relevant_categories
    
    def _get_baseline_value(self, category: ImpactCategory, current_state: Dict[str, Any]) -> float:
        """Get baseline value for impact category from current state"""
        baselines = {
            ImpactCategory.FAN_SATISFACTION: current_state.get("avg_satisfaction", 70.0),
            ImpactCategory.WAIT_TIME_REDUCTION: current_state.get("avg_queue_time", 15.0),
            ImpactCategory.SAFETY_IMPROVEMENT: current_state.get("safety_score", 85.0),
            ImpactCategory.EFFICIENCY_GAIN: current_state.get("operational_efficiency", 75.0),
            ImpactCategory.REVENUE_INCREASE: current_state.get("hourly_revenue", 5000.0),
            ImpactCategory.RISK_MITIGATION: current_state.get("risk_level", 20.0),
            ImpactCategory.CARBON_REDUCTION: current_state.get("carbon_rate", 100.0),
            ImpactCategory.ACCESSIBILITY_ENHANCEMENT: current_state.get("accessibility_score", 80.0)
        }
        
        return baselines.get(category, 50.0)
    
    async def _estimate_improvement(
        self,
        proposal: InterventionProposal,
        category: ImpactCategory, 
        baseline_value: float,
        current_state: Dict[str, Any]
    ) -> float:
        """Estimate improvement for specific impact category"""
        
        # Base improvement estimates by intervention type and category
        improvement_matrix = {
            (InterventionType.VOLUNTEER_DEPLOYMENT, ImpactCategory.FAN_SATISFACTION): 15.0,
            (InterventionType.VOLUNTEER_DEPLOYMENT, ImpactCategory.WAIT_TIME_REDUCTION): -8.0,  # Reduction
            (InterventionType.GATE_OPERATION, ImpactCategory.WAIT_TIME_REDUCTION): -12.0,
            (InterventionType.GATE_OPERATION, ImpactCategory.SAFETY_IMPROVEMENT): 10.0,
            (InterventionType.COMMUNICATION, ImpactCategory.FAN_SATISFACTION): 8.0,
            (InterventionType.COMMUNICATION, ImpactCategory.RISK_MITIGATION): -15.0,  # Risk reduction
            (InterventionType.QUEUE_MANAGEMENT, ImpactCategory.WAIT_TIME_REDUCTION): -20.0,
            (InterventionType.QUEUE_MANAGEMENT, ImpactCategory.FAN_SATISFACTION): 12.0
        }
        
        base_improvement = improvement_matrix.get(
            (proposal.intervention_type, category), 
            5.0  # Default modest improvement
        )
        
        # Scale improvement based on affected fans and confidence
        fan_scale = min(2.0, proposal.get_total_fans_affected() / 500.0)  # More fans = more impact
        confidence_scale = proposal.success_probability
        
        scaled_improvement = base_improvement * fan_scale * confidence_scale
        
        # Return new predicted value
        if category in [ImpactCategory.WAIT_TIME_REDUCTION, ImpactCategory.RISK_MITIGATION]:
            # These categories represent reductions, so improvement is negative
            return max(0, baseline_value + scaled_improvement)
        else:
            # These categories represent increases
            return baseline_value + abs(scaled_improvement)
    
    def _calculate_impact_confidence(self, proposal: InterventionProposal, category: ImpactCategory) -> float:
        """Calculate confidence in impact prediction for specific category"""
        
        # Base confidence by intervention type
        base_confidence = {
            InterventionType.COMMUNICATION: 0.85,  # High confidence - direct impact
            InterventionType.VOLUNTEER_DEPLOYMENT: 0.75,
            InterventionType.QUEUE_MANAGEMENT: 0.8,
            InterventionType.GATE_OPERATION: 0.7,
            InterventionType.RESOURCE_ALLOCATION: 0.6,
            InterventionType.TRANSPORT_ADJUSTMENT: 0.5,  # Many external factors
            InterventionType.FACILITY_OPERATION: 0.65,
            InterventionType.EMERGENCY_PREPARATION: 0.9  # High confidence in safety impact
        }.get(proposal.intervention_type, 0.7)
        
        # Adjust confidence based on category alignment
        category_alignment = {
            # How well each category aligns with intervention types
            ImpactCategory.SAFETY_IMPROVEMENT: 0.9,
            ImpactCategory.FAN_SATISFACTION: 0.8,
            ImpactCategory.WAIT_TIME_REDUCTION: 0.85,
            ImpactCategory.EFFICIENCY_GAIN: 0.75,
            ImpactCategory.RISK_MITIGATION: 0.8,
            ImpactCategory.REVENUE_INCREASE: 0.6,  # Harder to predict
            ImpactCategory.CARBON_REDUCTION: 0.5,  # Many variables
            ImpactCategory.ACCESSIBILITY_ENHANCEMENT: 0.7
        }.get(category, 0.7)
        
        # Combine confidences
        final_confidence = (base_confidence * 0.6 + category_alignment * 0.4) * proposal.success_probability
        
        return min(1.0, max(0.1, final_confidence))
    
    def _estimate_fans_affected(self, proposal: InterventionProposal, category: ImpactCategory, current_state: Dict[str, Any]) -> int:
        """Estimate number of fans affected by intervention for specific category"""
        
        total_fans = current_state.get("total_fans", 10000)
        
        # Base affected percentages by intervention type
        affected_percentages = {
            InterventionType.COMMUNICATION: 0.8,  # Announcements reach most fans
            InterventionType.GATE_OPERATION: 0.3,  # Affects fans using specific gates
            InterventionType.VOLUNTEER_DEPLOYMENT: 0.1,  # Local impact
            InterventionType.QUEUE_MANAGEMENT: 0.2,  # Affects queuing fans
            InterventionType.TRANSPORT_ADJUSTMENT: 0.6,  # Affects arriving/departing fans
            InterventionType.FACILITY_OPERATION: 0.15,  # Affects facility users
            InterventionType.EMERGENCY_PREPARATION: 1.0,  # Potentially affects everyone
            InterventionType.RESOURCE_ALLOCATION: 0.25
        }.get(proposal.intervention_type, 0.2)
        
        # Scale based on urgency (urgent interventions often affect more people)
        urgency_multiplier = 1.0 + (proposal.urgency_score * 0.5)
        
        affected_fans = int(total_fans * affected_percentages * urgency_multiplier)
        
        return max(10, min(total_fans, affected_fans))  # Between 10 and total fans
    
    def _estimate_impact_duration(self, proposal: InterventionProposal, category: ImpactCategory) -> int:
        """Estimate how long the intervention impact will last (in minutes)"""
        
        # Base durations by intervention type
        base_durations = {
            InterventionType.COMMUNICATION: 30,  # Effect lasts while information is relevant
            InterventionType.VOLUNTEER_DEPLOYMENT: 120,  # While volunteer is active
            InterventionType.GATE_OPERATION: 90,  # Until flow patterns change
            InterventionType.QUEUE_MANAGEMENT: 60,  # Until queue conditions change  
            InterventionType.TRANSPORT_ADJUSTMENT: 180,  # Affects multiple transport cycles
            InterventionType.FACILITY_OPERATION: 240,  # Facility changes have longer impact
            InterventionType.EMERGENCY_PREPARATION: 480,  # Safety measures remain active
            InterventionType.RESOURCE_ALLOCATION: 150
        }.get(proposal.intervention_type, 90)
        
        # Some categories have inherently different durations
        category_modifiers = {
            ImpactCategory.SAFETY_IMPROVEMENT: 2.0,  # Safety improvements last longer
            ImpactCategory.RISK_MITIGATION: 1.8,
            ImpactCategory.ACCESSIBILITY_ENHANCEMENT: 1.5,
            ImpactCategory.WAIT_TIME_REDUCTION: 0.8,  # Queue effects are temporary
            ImpactCategory.FAN_SATISFACTION: 1.2,
            ImpactCategory.EFFICIENCY_GAIN: 1.3,
            ImpactCategory.REVENUE_INCREASE: 1.0,
            ImpactCategory.CARBON_REDUCTION: 1.0
        }.get(category, 1.0)
        
        return int(base_durations * category_modifiers)
    
    def _generate_impact_description(self, proposal: InterventionProposal, category: ImpactCategory, improvement_delta: float) -> str:
        """Generate natural language description of expected impact"""
        
        impact_direction = "increase" if improvement_delta > 0 else "decrease" 
        impact_magnitude = abs(improvement_delta)
        
        if impact_magnitude < 5:
            magnitude_desc = "slight"
        elif impact_magnitude < 15:
            magnitude_desc = "moderate" 
        elif impact_magnitude < 30:
            magnitude_desc = "significant"
        else:
            magnitude_desc = "major"
        
        category_descriptions = {
            ImpactCategory.FAN_SATISFACTION: f"{magnitude_desc} {impact_direction} in fan satisfaction scores",
            ImpactCategory.WAIT_TIME_REDUCTION: f"{magnitude_desc} reduction in average wait times",
            ImpactCategory.SAFETY_IMPROVEMENT: f"{magnitude_desc} improvement in safety metrics",
            ImpactCategory.EFFICIENCY_GAIN: f"{magnitude_desc} increase in operational efficiency",
            ImpactCategory.RISK_MITIGATION: f"{magnitude_desc} reduction in identified risks",
            ImpactCategory.REVENUE_INCREASE: f"{magnitude_desc} increase in revenue generation",
            ImpactCategory.CARBON_REDUCTION: f"{magnitude_desc} reduction in carbon footprint",
            ImpactCategory.ACCESSIBILITY_ENHANCEMENT: f"{magnitude_desc} improvement in accessibility"
        }
        
        return category_descriptions.get(category, f"{magnitude_desc} positive impact expected")
    
    def _generate_success_indicators(self, proposal: InterventionProposal, category: ImpactCategory) -> List[str]:
        """Generate measurable success indicators for impact category"""
        
        indicator_templates = {
            ImpactCategory.FAN_SATISFACTION: [
                "Fan satisfaction surveys show improvement",
                "Reduced complaints and negative feedback",
                "Increased positive social media mentions"
            ],
            ImpactCategory.WAIT_TIME_REDUCTION: [
                "Queue sensors show reduced wait times",
                "Faster service completion rates",
                "Reduced queue abandonment rates"
            ],
            ImpactCategory.SAFETY_IMPROVEMENT: [
                "No safety incidents in affected area",
                "Improved crowd density distribution",
                "Faster emergency response times"
            ],
            ImpactCategory.EFFICIENCY_GAIN: [
                "Higher throughput rates",
                "Reduced resource waste",
                "Improved staff productivity metrics"
            ],
            ImpactCategory.RISK_MITIGATION: [
                "Zero incidents of identified risks",
                "Improved safety compliance scores",
                "Faster hazard resolution times"
            ]
        }
        
        return indicator_templates.get(category, [
            "Measurable improvement in target metrics",
            "Positive feedback from stakeholders",
            "No negative side effects observed"
        ])
    
    def _identify_risk_factors(self, proposal: InterventionProposal, category: ImpactCategory) -> List[str]:
        """Identify potential risk factors that could affect intervention success"""
        
        # General risk factors by intervention type
        type_risks = {
            InterventionType.VOLUNTEER_DEPLOYMENT: [
                "Volunteer unavailability",
                "Communication breakdowns",
                "Task complexity exceeding volunteer skills"
            ],
            InterventionType.GATE_OPERATION: [
                "Security protocol conflicts",
                "Unexpected crowd surge",
                "Technical gate malfunctions"
            ],
            InterventionType.COMMUNICATION: [
                "Language barriers",
                "PA system failures",
                "Information accuracy issues"
            ],
            InterventionType.QUEUE_MANAGEMENT: [
                "Fan resistance to queue changes",
                "Insufficient crowd control resources",
                "Competing priority areas"
            ]
        }
        
        base_risks = type_risks.get(proposal.intervention_type, [
            "Resource availability changes",
            "Unexpected external factors",
            "Implementation timing issues"
        ])
        
        # Add category-specific risks
        category_risks = {
            ImpactCategory.SAFETY_IMPROVEMENT: ["Safety protocol conflicts"],
            ImpactCategory.FAN_SATISFACTION: ["Fan expectation mismatches"],
            ImpactCategory.EFFICIENCY_GAIN: ["System integration issues"],
            ImpactCategory.REVENUE_INCREASE: ["Economic condition changes"]
        }
        
        if category in category_risks:
            base_risks.extend(category_risks[category])
        
        return base_risks[:4]  # Max 4 risk factors
    
    def _monetize_revenue_impact(self, assessment: ImpactAssessment) -> float:
        """Convert revenue impact assessment to monetary value"""
        improvement = abs(assessment.predicted_improvement - assessment.current_baseline)
        base_value_per_fan = 25.0  # Average spending per fan
        
        revenue_benefit = (
            assessment.fans_affected * 
            base_value_per_fan * 
            (improvement / 100.0) * 
            assessment.confidence
        )
        
        return revenue_benefit
    
    def _monetize_efficiency_impact(self, assessment: ImpactAssessment) -> float:
        """Convert efficiency impact to monetary savings"""
        improvement = abs(assessment.predicted_improvement - assessment.current_baseline)
        efficiency_value_per_percent = 50.0  # $50 value per efficiency percent
        
        efficiency_benefit = (
            improvement * 
            efficiency_value_per_percent * 
            assessment.confidence
        )
        
        return efficiency_benefit
    
    def _monetize_satisfaction_impact(self, assessment: ImpactAssessment) -> float:
        """Convert fan satisfaction impact to monetary value"""
        improvement = abs(assessment.predicted_improvement - assessment.current_baseline)
        satisfaction_value_per_fan = 3.0  # $3 per satisfaction point per fan
        
        satisfaction_benefit = (
            assessment.fans_affected * 
            satisfaction_value_per_fan * 
            (improvement / 100.0) *
            assessment.confidence
        )
        
        return satisfaction_benefit
    
    def _monetize_risk_impact(self, assessment: ImpactAssessment) -> float:
        """Convert risk mitigation to monetary value"""
        improvement = abs(assessment.predicted_improvement - assessment.current_baseline)
        risk_cost_per_incident = 1000.0  # Cost of average incident
        incident_probability = 0.1  # 10% chance of incident per risk point
        
        risk_benefit = (
            improvement * 
            incident_probability * 
            risk_cost_per_incident * 
            assessment.confidence
        )
        
        return risk_benefit
    
    def _monetize_carbon_impact(self, assessment: ImpactAssessment) -> float:
        """Convert carbon reduction to monetary value"""
        improvement = abs(assessment.predicted_improvement - assessment.current_baseline)
        carbon_price_per_ton = 25.0  # $25 per ton CO2
        kg_per_point = 10.0  # 10kg CO2 per improvement point
        
        carbon_tons = (improvement * kg_per_point) / 1000.0
        carbon_benefit = carbon_tons * carbon_price_per_ton * assessment.confidence
        
        return carbon_benefit
    
    def _calculate_resource_cost(self, proposal: InterventionProposal) -> float:
        """Calculate direct resource cost for intervention"""
        base_costs = {
            InterventionType.VOLUNTEER_DEPLOYMENT: 15.0,
            InterventionType.GATE_OPERATION: 5.0,
            InterventionType.COMMUNICATION: 2.0,
            InterventionType.QUEUE_MANAGEMENT: 8.0,
            InterventionType.RESOURCE_ALLOCATION: 12.0,
            InterventionType.TRANSPORT_ADJUSTMENT: 20.0,
            InterventionType.FACILITY_OPERATION: 10.0,
            InterventionType.EMERGENCY_PREPARATION: 25.0
        }.get(proposal.intervention_type, 10.0)
        
        # Scale by complexity and resource requirements
        complexity_multiplier = 1.0 + proposal.complexity_score
        resource_multiplier = 1.0 + len(proposal.resource_requirements) * 0.1
        
        return base_costs * complexity_multiplier * resource_multiplier