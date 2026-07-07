"""
StadiumVerse AI V2 - Debate Chamber
The core debate orchestration system where AI agents argue and reason
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

from .debate_models import DebateSession, AgentPosition, DebateDecision, AgentRole, DebateStatus
from ..providers.factory import get_global_ai_provider
from ...config import settings

logger = logging.getLogger(__name__)

class DebateChamber:
    """
    The Living Brain's debate chamber where AI agents engage in structured argumentation
    """
    
    def __init__(self):
        self.active_debates: Dict[str, DebateSession] = {}
        self.debate_history: List[DebateSession] = []
        self.agent_system_prompts = self._initialize_agent_prompts()
        
    def _initialize_agent_prompts(self) -> Dict[AgentRole, str]:
        """Initialize system prompts for each agent type"""
        return {
            AgentRole.NAVIGATION: """
You are the Navigation Agent in StadiumVerse AI's debate chamber. Your expertise is crowd flow, pathfinding, and movement optimization.

In debates, provide:
1. Clear reasoning based on crowd density data
2. Confidence level (0-100%)  
3. Risk assessment for movement patterns
4. Alternative routing options
5. Estimated impact on fan flow
6. Cost analysis of navigation changes

Always consider accessibility needs and emergency evacuation routes.
Be specific with numbers, timeframes, and affected fan counts.
""",
            AgentRole.SECURITY: """
You are the Security Agent in StadiumVerse AI's debate chamber. Your expertise is threat assessment, crowd safety, and risk management.

In debates, provide:
1. Security risk analysis with specific threat levels
2. Confidence in risk assessment (0-100%)
3. Crowd safety implications 
4. Alternative security measures
5. Resource requirements (personnel, equipment)
6. Timeline for implementation

Prioritize fan safety while balancing operational efficiency.
Consider VIP movements, emergency protocols, and crowd psychology.
""",
            AgentRole.MEDICAL: """  
You are the Medical Agent in StadiumVerse AI's debate chamber. Your expertise is health monitoring, emergency response, and medical risk assessment.

In debates, provide:
1. Medical risk analysis based on fan health data
2. Confidence in medical predictions (0-100%)
3. Emergency response time implications
4. Alternative medical deployment strategies  
5. Resource needs (staff, equipment, ambulances)
6. Patient outcome projections

Focus on minimizing response times and maximizing medical coverage.
Consider accessibility for medical equipment and evacuation routes.
""",
            AgentRole.VOLUNTEER: """
You are the Volunteer Agent in StadiumVerse AI's debate chamber. Your expertise is human resource optimization and task coordination.

In debates, provide:
1. Volunteer availability and skill analysis
2. Confidence in deployment success (0-100%)
3. Task completion risk assessment
4. Alternative staffing approaches
5. Training and coordination requirements
6. Fan satisfaction impact

Balance volunteer workload with operational needs.
Consider language skills, specialization, and volunteer well-being.
""",
            AgentRole.FOOD: """
You are the Food Service Agent in StadiumVerse AI's debate chamber. Your expertise is concession management, demand forecasting, and supply optimization.

In debates, provide:
1. Demand prediction and supply analysis  
2. Confidence in service capacity (0-100%)
3. Queue management risk assessment
4. Alternative service strategies
5. Revenue and cost implications
6. Fan satisfaction projections

Optimize for reduced wait times and maximum satisfaction.
Consider dietary restrictions, cultural preferences, and peak demand periods.
""",
            AgentRole.TRANSPORT: """
You are the Transport Agent in StadiumVerse AI's debate chamber. Your expertise is transportation coordination, traffic flow, and arrival/departure optimization.

In debates, provide:
1. Transportation capacity and timing analysis
2. Confidence in traffic predictions (0-100%) 
3. Congestion risk assessment
4. Alternative transport routing
5. Infrastructure utilization optimization
6. Environmental impact considerations

Focus on smooth fan arrival and departure experiences.
Coordinate with external transport authorities and real-time traffic data.
""",
            AgentRole.ACCESSIBILITY: """
You are the Accessibility Agent in StadiumVerse AI's debate chamber. Your expertise is inclusive design, disability accommodation, and barrier-free access.

In debates, provide:
1. Accessibility impact analysis for all fans
2. Confidence in accommodation effectiveness (0-100%)
3. Barrier and compliance risk assessment  
4. Alternative inclusive solutions
5. Specialized resource requirements
6. Legal compliance implications

Ensure all decisions consider fans with disabilities.
Advocate for universal design principles and proactive accommodation.
""",
            AgentRole.WEATHER: """
You are the Weather Agent in StadiumVerse AI's debate chamber. Your expertise is meteorological analysis, environmental impact, and weather-related risk management.

In debates, provide:
1. Weather impact prediction and analysis
2. Confidence in weather forecasts (0-100%)
3. Environmental risk assessment
4. Alternative weather mitigation strategies
5. Infrastructure and safety implications  
6. Fan comfort and safety projections

Consider both immediate and extended weather impacts.
Integrate real-time data with predictive meteorological models.
""",
            AgentRole.SUSTAINABILITY: """
You are the Sustainability Agent in StadiumVerse AI's debate chamber. Your expertise is environmental impact, carbon footprint optimization, and resource efficiency.

In debates, provide:
1. Environmental impact analysis
2. Confidence in sustainability metrics (0-100%)
3. Carbon footprint risk assessment
4. Alternative eco-friendly approaches
5. Resource consumption implications
6. Long-term environmental benefits

Balance operational efficiency with environmental responsibility.
Quantify carbon savings, waste reduction, and resource optimization.
""",
            AgentRole.EMERGENCY: """
You are the Emergency Response Agent in StadiumVerse AI's debate chamber. Your expertise is crisis management, evacuation planning, and emergency coordination.

In debates, provide:
1. Emergency preparedness analysis
2. Confidence in response effectiveness (0-100%)
3. Crisis escalation risk assessment
4. Alternative emergency protocols
5. Multi-agency coordination requirements
6. Recovery timeline projections

Prioritize life safety and rapid response capabilities.
Maintain readiness for multiple simultaneous emergencies.
""",
            AgentRole.CLEANING: """
You are the Cleaning and Maintenance Agent in StadiumVerse AI's debate chamber. Your expertise is facility maintenance, sanitation, and operational cleanliness.

In debates, provide:
1. Maintenance impact and cleanliness analysis
2. Confidence in service delivery (0-100%)
3. Hygiene and safety risk assessment
4. Alternative maintenance schedules
5. Resource and staffing requirements
6. Fan experience implications

Maintain high cleanliness standards while minimizing disruptions.
Consider health regulations, waste management, and facility preservation.
""",
            AgentRole.ANALYTICS: """
You are the Analytics Agent in StadiumVerse AI's debate chamber. Your expertise is data analysis, pattern recognition, and performance metrics.

In debates, provide:
1. Data-driven analysis and trend identification
2. Confidence in statistical predictions (0-100%)
3. Performance metric risk assessment
4. Alternative measurement approaches
5. ROI and effectiveness calculations
6. Benchmarking and improvement opportunities

Ground all arguments in quantitative data and historical patterns.
Provide objective analysis to support evidence-based decision making.
"""
        }
    
    async def initiate_debate(
        self,
        topic: str,
        context: Dict[str, Any],
        trigger_event: str,
        urgency_level: int = 3,
        participating_agents: Optional[List[AgentRole]] = None
    ) -> DebateSession:
        """
        Initiate a new debate session
        
        Args:
            topic: The decision topic to debate
            context: Relevant context data
            trigger_event: What triggered this debate
            urgency_level: 1-5 urgency scale
            participating_agents: Which agents should participate
            
        Returns:
            DebateSession: The initiated debate session
        """
        if participating_agents is None:
            # Default: all agents except coordinator participate
            participating_agents = [role for role in AgentRole if role != AgentRole.COORDINATOR]
        
        debate_session = DebateSession(
            topic=topic,
            context=context,
            trigger_event=trigger_event,
            urgency_level=urgency_level
        )
        
        self.active_debates[debate_session.session_id] = debate_session
        
        logger.info(f"Initiated debate session {debate_session.session_id}: {topic}")
        
        try:
            # Gather positions from all participating agents
            await self._gather_agent_positions(debate_session, participating_agents)
            
            # Generate final decision through coordinator
            await self._generate_final_decision(debate_session)
            
            # Move to debate history
            self.debate_history.append(debate_session)
            if len(self.debate_history) > 100:  # Keep last 100 debates
                self.debate_history = self.debate_history[-100:]
            
            del self.active_debates[debate_session.session_id]
            
            return debate_session
            
        except Exception as e:
            logger.error(f"Error in debate session {debate_session.session_id}: {e}")
            debate_session.status = DebateStatus.OVERRIDDEN
            raise
    
    async def _gather_agent_positions(self, debate_session: DebateSession, agents: List[AgentRole]):
        """Gather positions from all participating agents"""
        ai_provider = await get_global_ai_provider()
        
        # Create debate context message
        context_message = f"""
DEBATE TOPIC: {debate_session.topic}

TRIGGER EVENT: {debate_session.trigger_event}

CURRENT SITUATION:
{self._format_context_for_agents(debate_session.context)}

URGENCY LEVEL: {debate_session.urgency_level}/5

Provide your position with:
1. Your specific recommendation
2. Clear reasoning with supporting data
3. Confidence level (0-100%)
4. Risk assessment (low/medium/high/critical)
5. Alternative actions you would support
6. Estimated cost/resources needed
7. Expected impact on fans and operations

Be specific, actionable, and data-driven.
"""
        
        # Gather positions concurrently for efficiency
        position_tasks = []
        for agent_role in agents:
            if agent_role in self.agent_system_prompts:
                task = self._get_agent_position(
                    ai_provider, 
                    agent_role, 
                    context_message,
                    debate_session.context
                )
                position_tasks.append(task)
        
        # Wait for all agent positions
        positions = await asyncio.gather(*position_tasks, return_exceptions=True)
        
        # Add successful positions to debate
        for i, position in enumerate(positions):
            if isinstance(position, AgentPosition):
                debate_session.add_agent_position(position)
            else:
                logger.error(f"Failed to get position from agent {agents[i]}: {position}")
    
    async def _get_agent_position(
        self, 
        ai_provider, 
        agent_role: AgentRole, 
        context_message: str,
        debate_context: Dict[str, Any]
    ) -> AgentPosition:
        """Get position from a specific agent"""
        try:
            system_prompt = self.agent_system_prompts[agent_role]
            
            response = await ai_provider.generate_debate_response(
                agent_name=agent_role.value,
                system_prompt=system_prompt,
                debate_context={
                    "message": context_message,
                    **debate_context
                }
            )
            
            # Parse response into structured position
            return self._parse_agent_response(agent_role, response.content, response.confidence)
            
        except Exception as e:
            logger.error(f"Error getting position from {agent_role.value}: {e}")
            
            # Return fallback position
            return AgentPosition(
                agent_name=agent_role,
                recommendation="Unable to generate recommendation",
                reasoning=f"Technical error: {str(e)}",
                confidence=0.0,
                risk_assessment="unknown",
                alternative_actions=["Manual decision required"],
                estimated_cost=0.0,
                estimated_impact="Unknown impact due to agent error"
            )
    
    def _parse_agent_response(self, agent_role: AgentRole, content: str, ai_confidence: float) -> AgentPosition:
        """Parse AI response into structured AgentPosition"""
        lines = content.strip().split('\n')
        
        # Default values
        recommendation = "No specific recommendation provided"
        reasoning = content[:200] + "..." if len(content) > 200 else content
        confidence = ai_confidence
        risk_assessment = "medium"
        alternatives = []
        cost = 0.0
        impact = "Impact assessment pending"
        
        # Parse structured response
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            line_lower = line.lower()
            
            # Detect sections
            if any(keyword in line_lower for keyword in ['recommendation', 'suggest', 'propose']):
                current_section = 'recommendation'
                # Extract recommendation from same line if present
                if ':' in line:
                    recommendation = line.split(':', 1)[1].strip()
                continue
            elif any(keyword in line_lower for keyword in ['reason', 'because', 'analysis']):
                current_section = 'reasoning'
                if ':' in line:
                    reasoning = line.split(':', 1)[1].strip()
                continue
            elif 'confidence' in line_lower:
                current_section = 'confidence'
                # Extract confidence percentage
                import re
                conf_match = re.search(r'(\d+(?:\.\d+)?)', line)
                if conf_match:
                    conf_val = float(conf_match.group(1))
                    confidence = conf_val / 100.0 if conf_val > 1.0 else conf_val
                continue
            elif 'risk' in line_lower:
                current_section = 'risk'
                if any(level in line_lower for level in ['low', 'medium', 'high', 'critical']):
                    for level in ['critical', 'high', 'medium', 'low']:  # Check in priority order
                        if level in line_lower:
                            risk_assessment = level
                            break
                continue
            elif any(keyword in line_lower for keyword in ['alternative', 'option', 'instead']):
                current_section = 'alternatives'
                alternatives.append(line)
                continue
            elif any(keyword in line_lower for keyword in ['cost', 'resource', 'budget']):
                current_section = 'cost'
                # Extract cost if numeric value present
                import re
                cost_match = re.search(r'[\$]?(\d+(?:\.\d+)?)', line)
                if cost_match:
                    cost = float(cost_match.group(1))
                continue
            elif 'impact' in line_lower:
                current_section = 'impact'
                if ':' in line:
                    impact = line.split(':', 1)[1].strip()
                continue
            
            # Add content to current section
            if current_section == 'recommendation' and len(line) > 10:
                recommendation = line
            elif current_section == 'reasoning' and len(line) > 10:
                reasoning += " " + line
            elif current_section == 'alternatives':
                alternatives.append(line)
            elif current_section == 'impact' and len(line) > 10:
                impact = line
        
        # Ensure we have alternatives
        if not alternatives:
            alternatives = [
                "Maintain current approach",
                "Escalate to manual review", 
                "Implement partial solution"
            ]
        
        return AgentPosition(
            agent_name=agent_role,
            recommendation=recommendation,
            reasoning=reasoning[:500],  # Limit reasoning length
            confidence=min(1.0, max(0.0, confidence)),
            risk_assessment=risk_assessment,
            alternative_actions=alternatives[:3],  # Max 3 alternatives
            estimated_cost=cost,
            estimated_impact=impact[:200]  # Limit impact description
        )
    
    async def _generate_final_decision(self, debate_session: DebateSession):
        """Generate final coordinated decision based on all agent positions"""
        ai_provider = await get_global_ai_provider()
        
        # Prepare coordinator context
        coordinator_context = self._prepare_coordinator_context(debate_session)
        
        coordinator_prompt = """
You are the Coordinator Agent for StadiumVerse AI. Your role is to synthesize all agent positions and make the final decision.

Based on the agent debate below, provide a final decision that:
1. Considers all agent perspectives
2. Balances competing priorities  
3. Minimizes risk while maximizing benefit
4. Provides clear implementation steps
5. Includes fallback plans
6. Estimates resource requirements and timeline

Format your response with:
- DECISION: Clear final decision
- REASONING: Why this decision was chosen
- CONFIDENCE: Your confidence level (0-100%)
- RISK_LEVEL: low/medium/high/critical
- IMPLEMENTATION: Step-by-step implementation plan
- TIMELINE: Expected implementation timeline
- SUCCESS_PROBABILITY: Likelihood of success (0-100%)
- FALLBACK: What to do if this fails
- AFFECTED_FANS: Number of fans impacted
- RESOURCES: Required resources and personnel
"""
        
        try:
            response = await ai_provider.generate_agent_response(
                agent_name="coordinator",
                system_prompt=coordinator_prompt,
                user_message=coordinator_context
            )
            
            # Parse coordinator response into decision
            decision = self._parse_coordinator_decision(response.content, debate_session)
            debate_session.conclude_debate(decision)
            
        except Exception as e:
            logger.error(f"Error generating coordinator decision: {e}")
            
            # Fallback decision
            fallback_decision = DebateDecision(
                decision="Manual review required",
                reasoning=f"Automated decision failed: {str(e)}",
                confidence=0.0,
                risk_level="high",
                implementation_steps=["Escalate to human operators", "Review agent positions manually"],
                estimated_timeline="Immediate",
                success_probability=0.5,
                fallback_plan="Human override and manual decision making",
                affected_fans=0,
                resource_requirements=["Human operator time"]
            )
            
            debate_session.conclude_debate(fallback_decision)
    
    def _prepare_coordinator_context(self, debate_session: DebateSession) -> str:
        """Prepare context summary for coordinator decision"""
        context_parts = [
            f"DEBATE TOPIC: {debate_session.topic}",
            f"TRIGGER: {debate_session.trigger_event}",
            f"URGENCY: {debate_session.urgency_level}/5",
            f"PARTICIPATING AGENTS: {len(debate_session.agent_positions)}",
            "",
            "AGENT POSITIONS:",
        ]
        
        for position in debate_session.agent_positions:
            context_parts.extend([
                f"\n{position.agent_name.value.upper()} AGENT:",
                f"Recommendation: {position.recommendation}",
                f"Reasoning: {position.reasoning}",
                f"Confidence: {position.confidence:.0%}",
                f"Risk: {position.risk_assessment}",
                f"Alternatives: {', '.join(position.alternative_actions[:2])}",
                f"Cost: ${position.estimated_cost:.0f}",
                f"Impact: {position.estimated_impact}",
            ])
        
        context_parts.extend([
            "",
            f"CONSENSUS SCORE: {debate_session.get_consensus_score():.0%}",
            f"RISK DISTRIBUTION: {debate_session.get_risk_distribution()}",
            "",
            "Make your final coordinated decision considering all perspectives."
        ])
        
        return "\n".join(context_parts)
    
    def _parse_coordinator_decision(self, content: str, debate_session: DebateSession) -> DebateDecision:
        """Parse coordinator response into structured decision"""
        lines = content.strip().split('\n')
        
        # Default values
        decision = "Review required"
        reasoning = "Unable to parse coordinator decision"
        confidence = 0.5
        risk_level = "medium"
        implementation_steps = []
        timeline = "Unknown"
        success_probability = 0.5
        fallback_plan = "Manual intervention"
        affected_fans = 0
        resources = []
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            # Parse sections
            if line_lower.startswith('decision:'):
                decision = line.split(':', 1)[1].strip()
            elif line_lower.startswith('reasoning:'):
                reasoning = line.split(':', 1)[1].strip()
            elif line_lower.startswith('confidence:'):
                import re
                conf_match = re.search(r'(\d+)', line)
                if conf_match:
                    confidence = float(conf_match.group(1)) / 100.0
            elif line_lower.startswith('risk_level:'):
                risk_level = line.split(':', 1)[1].strip().lower()
            elif line_lower.startswith('implementation:'):
                current_section = 'implementation'
                impl_text = line.split(':', 1)[1].strip()
                if impl_text:
                    implementation_steps.append(impl_text)
            elif line_lower.startswith('timeline:'):
                timeline = line.split(':', 1)[1].strip()
            elif line_lower.startswith('success_probability:'):
                import re
                prob_match = re.search(r'(\d+)', line)
                if prob_match:
                    success_probability = float(prob_match.group(1)) / 100.0
            elif line_lower.startswith('fallback:'):
                fallback_plan = line.split(':', 1)[1].strip()
            elif line_lower.startswith('affected_fans:'):
                import re
                fans_match = re.search(r'(\d+)', line)
                if fans_match:
                    affected_fans = int(fans_match.group(1))
            elif line_lower.startswith('resources:'):
                current_section = 'resources'
                res_text = line.split(':', 1)[1].strip()
                if res_text:
                    resources.append(res_text)
            elif current_section == 'implementation' and line.startswith('-'):
                implementation_steps.append(line[1:].strip())
            elif current_section == 'resources' and line.startswith('-'):
                resources.append(line[1:].strip())
        
        # Calculate ROI analysis
        roi_analysis = {
            "estimated_benefit": affected_fans * 0.1,  # Rough benefit estimate
            "cost_per_fan": resources and len(resources) * 10 or 0,
            "payback_period": "1-2 hours",
            "risk_adjusted_roi": success_probability * 1.5
        }
        
        return DebateDecision(
            decision=decision,
            reasoning=reasoning,
            confidence=confidence,
            risk_level=risk_level,
            implementation_steps=implementation_steps if implementation_steps else ["Execute decision"],
            estimated_timeline=timeline,
            success_probability=success_probability,
            fallback_plan=fallback_plan,
            affected_fans=affected_fans,
            resource_requirements=resources if resources else ["Standard operational resources"],
            roi_analysis=roi_analysis,
            carbon_impact=0.0  # TODO: Calculate based on decision type
        )
    
    def _format_context_for_agents(self, context: Dict[str, Any]) -> str:
        """Format context data for agent consumption"""
        formatted_parts = []
        
        for key, value in context.items():
            if isinstance(value, dict):
                formatted_parts.append(f"{key.upper()}:")
                for sub_key, sub_value in value.items():
                    formatted_parts.append(f"  {sub_key}: {sub_value}")
            elif isinstance(value, list):
                formatted_parts.append(f"{key.upper()}: {', '.join(map(str, value))}")
            else:
                formatted_parts.append(f"{key.upper()}: {value}")
        
        return "\n".join(formatted_parts)
    
    def get_recent_debates(self, limit: int = 10) -> List[DebateSession]:
        """Get recent debate sessions"""
        return sorted(self.debate_history, key=lambda d: d.started_at, reverse=True)[:limit]
    
    def get_debate_by_id(self, session_id: str) -> Optional[DebateSession]:
        """Get specific debate session by ID"""
        # Check active debates first
        if session_id in self.active_debates:
            return self.active_debates[session_id]
        
        # Check history
        for debate in self.debate_history:
            if debate.session_id == session_id:
                return debate
        
        return None
    
    async def quick_consensus_check(
        self, 
        topic: str, 
        context: Dict[str, Any],
        agents: List[AgentRole] = None
    ) -> Dict[str, Any]:
        """Quick consensus check without full debate (for low-urgency decisions)"""
        if agents is None:
            agents = [AgentRole.NAVIGATION, AgentRole.SECURITY, AgentRole.MEDICAL]
        
        ai_provider = await get_global_ai_provider()
        quick_responses = []
        
        simple_prompt = f"Quick assessment for: {topic}\nContext: {context}\nProvide: recommendation, confidence (0-100%), risk level."
        
        for agent_role in agents:
            try:
                response = await ai_provider.generate_agent_response(
                    agent_name=agent_role.value,
                    system_prompt=self.agent_system_prompts[agent_role],
                    user_message=simple_prompt
                )
                
                quick_responses.append({
                    "agent": agent_role.value,
                    "response": response.content[:100],
                    "confidence": response.confidence
                })
                
            except Exception as e:
                logger.warning(f"Quick consensus failed for {agent_role}: {e}")
        
        return {
            "topic": topic,
            "quick_consensus": quick_responses,
            "avg_confidence": sum(r["confidence"] for r in quick_responses) / len(quick_responses) if quick_responses else 0,
            "requires_full_debate": len(quick_responses) < len(agents) * 0.7  # If >30% agents failed
        }