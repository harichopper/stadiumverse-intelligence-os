"""
StadiumVerse AI - Coordinator Agent
The master AI agent that coordinates all other agents and generates strategic insights
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import AsyncSessionLocal
from ...models.fan import DigitalFan, FanPrediction
from ...models.volunteer import Volunteer, VolunteerTask
from ...models.event import Emergency, AIInsight, CrowdAnalytics
from ...config import settings, AGENT_SYSTEM_PROMPTS
from ..llm.openai_client import OpenAIClient

# Import all specialized agents
from .navigation_agent import NavigationAgent
from .security_agent import SecurityAgent
from .medical_agent import MedicalAgent
from .volunteer_agent import VolunteerAgent
from .cleaning_agent import CleaningAgent
from .food_agent import FoodAgent
from .transport_agent import TransportAgent
from .accessibility_agent import AccessibilityAgent
from .weather_agent import WeatherAgent
from .sustainability_agent import SustainabilityAgent
from .emergency_agent import EmergencyAgent
from .analytics_agent import AnalyticsAgent

logger = logging.getLogger(__name__)

class CoordinatorAgent:
    """
    Master AI Coordinator that:
    - Manages all specialized agents
    - Synthesizes insights from multiple sources
    - Generates strategic recommendations
    - Coordinates emergency responses
    - Provides natural language explanations
    """
    
    def __init__(self):
        self.openai_client = OpenAIClient()
        
        # Initialize all specialized agents
        self.agents = {
            "navigation": NavigationAgent(),
            "security": SecurityAgent(), 
            "medical": MedicalAgent(),
            "volunteer": VolunteerAgent(),
            "cleaning": CleaningAgent(),
            "food": FoodAgent(),
            "transport": TransportAgent(),
            "accessibility": AccessibilityAgent(),
            "weather": WeatherAgent(),
            "sustainability": SustainabilityAgent(),
            "emergency": EmergencyAgent(),
            "analytics": AnalyticsAgent()
        }
        
        self.system_prompt = AGENT_SYSTEM_PROMPTS["coordinator"]
        
        # Performance tracking
        self.insights_generated = 0
        self.recommendations_implemented = 0
        self.accuracy_score = 0.0
        
        logger.info("Coordinator Agent initialized with 12 specialized agents")
    
    async def generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate comprehensive AI insights by coordinating all agents
        """
        try:
            # Gather data from all sources
            stadium_state = await self._gather_stadium_state()
            
            # Get insights from all specialized agents
            agent_insights = await self._gather_agent_insights(stadium_state)
            
            # Synthesize insights using LLM reasoning
            synthesized_insights = await self._synthesize_insights(stadium_state, agent_insights)
            
            # Generate strategic recommendations
            recommendations = await self._generate_recommendations(synthesized_insights)
            
            # Save insights to database
            await self._save_insights(synthesized_insights + recommendations)
            
            self.insights_generated += len(synthesized_insights + recommendations)
            
            return synthesized_insights + recommendations
            
        except Exception as e:
            logger.error(f"Error generating insights: {e}")
            return []
    
    async def _gather_stadium_state(self) -> Dict[str, Any]:
        """Gather current stadium state from database"""
        stadium_state = {
            "timestamp": datetime.utcnow().isoformat(),
            "fans": {},
            "volunteers": {},
            "emergencies": {},
            "predictions": {},
            "crowd_analytics": {},
            "weather": {},
            "performance": {}
        }
        
        async with AsyncSessionLocal() as session:
            # Get fan statistics
            fan_result = await session.execute(
                select(
                    func.count(DigitalFan.id).label('total_fans'),
                    func.avg(DigitalFan.stress_level).label('avg_stress'),
                    func.avg(DigitalFan.excitement_level).label('avg_excitement'),
                    func.avg(DigitalFan.fatigue_level).label('avg_fatigue'),
                    func.avg(DigitalFan.risk_score).label('avg_risk')
                ).where(DigitalFan.is_active == True)
            )
            fan_stats = fan_result.first()
            
            stadium_state["fans"] = {
                "total": fan_stats.total_fans,
                "avg_stress": float(fan_stats.avg_stress or 0),
                "avg_excitement": float(fan_stats.avg_excitement or 0),
                "avg_fatigue": float(fan_stats.avg_fatigue or 0),
                "avg_risk": float(fan_stats.avg_risk or 0)
            }
            
            # Get volunteer statistics
            volunteer_result = await session.execute(
                select(
                    func.count(Volunteer.id).label('total_volunteers'),
                    func.count(Volunteer.id).filter(Volunteer.availability_status == 'available').label('available_volunteers'),
                    func.count(Volunteer.id).filter(Volunteer.availability_status == 'busy').label('busy_volunteers')
                ).where(Volunteer.is_active == True)
            )
            volunteer_stats = volunteer_result.first()
            
            stadium_state["volunteers"] = {
                "total": volunteer_stats.total_volunteers,
                "available": volunteer_stats.available_volunteers,
                "busy": volunteer_stats.busy_volunteers,
                "utilization": (volunteer_stats.busy_volunteers / max(1, volunteer_stats.total_volunteers)) * 100
            }
            
            # Get active emergencies
            emergency_result = await session.execute(
                select(Emergency).where(Emergency.status == 'active').limit(10)
            )
            emergencies = emergency_result.scalars().all()
            
            stadium_state["emergencies"] = {
                "active_count": len(emergencies),
                "emergencies": [e.to_dict() for e in emergencies]
            }
            
            # Get recent predictions
            prediction_result = await session.execute(
                select(FanPrediction)
                .where(FanPrediction.created_at > datetime.utcnow() - timedelta(minutes=30))
                .limit(50)
            )
            predictions = prediction_result.scalars().all()
            
            stadium_state["predictions"] = {
                "recent_count": len(predictions),
                "avg_confidence": sum(p.confidence_score for p in predictions) / len(predictions) if predictions else 0
            }
        
        return stadium_state
    
    async def _gather_agent_insights(self, stadium_state: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Gather insights from all specialized agents"""
        agent_insights = {}
        
        # Run all agents concurrently for efficiency
        tasks = []
        for agent_name, agent in self.agents.items():
            task = asyncio.create_task(
                self._get_agent_insights(agent_name, agent, stadium_state)
            )
            tasks.append((agent_name, task))
        
        # Collect results
        for agent_name, task in tasks:
            try:
                insights = await task
                agent_insights[agent_name] = insights
            except Exception as e:
                logger.error(f"Error getting insights from {agent_name} agent: {e}")
                agent_insights[agent_name] = []
        
        return agent_insights
    
    async def _get_agent_insights(self, agent_name: str, agent, stadium_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get insights from a specific agent"""
        try:
            if hasattr(agent, 'generate_insights'):
                return await agent.generate_insights(stadium_state)
            else:
                # Fallback for agents without generate_insights method
                return await self._generate_basic_insights(agent_name, stadium_state)
        except Exception as e:
            logger.error(f"Error in {agent_name} agent: {e}")
            return []
    
    async def _generate_basic_insights(self, agent_name: str, stadium_state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate basic insights for agents without specialized methods"""
        insights = []
        
        # Basic insight based on agent type and stadium state
        fan_stats = stadium_state.get("fans", {})
        
        if agent_name == "navigation" and fan_stats.get("avg_stress", 0) > 70:
            insights.append({
                "type": "alert",
                "priority": 4,
                "title": "High Crowd Stress Detected",
                "description": f"Average fan stress level is {fan_stats.get('avg_stress', 0):.1f}%. Consider opening additional navigation routes.",
                "confidence": 0.8,
                "agent": agent_name
            })
        
        elif agent_name == "medical" and fan_stats.get("avg_risk", 0) > 60:
            insights.append({
                "type": "alert", 
                "priority": 5,
                "title": "Elevated Medical Risk",
                "description": f"Average fan risk score is {fan_stats.get('avg_risk', 0):.1f}%. Recommend additional medical staff deployment.",
                "confidence": 0.9,
                "agent": agent_name
            })
        
        elif agent_name == "security" and stadium_state.get("emergencies", {}).get("active_count", 0) > 0:
            insights.append({
                "type": "alert",
                "priority": 5, 
                "title": "Active Security Situations",
                "description": f"{stadium_state['emergencies']['active_count']} active emergencies require immediate attention.",
                "confidence": 1.0,
                "agent": agent_name
            })
        
        return insights
    
    async def _synthesize_insights(self, stadium_state: Dict[str, Any], agent_insights: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Use LLM to synthesize insights from all agents"""
        
        # Prepare context for LLM
        context = {
            "stadium_state": stadium_state,
            "agent_insights": agent_insights,
            "total_insights": sum(len(insights) for insights in agent_insights.values())
        }
        
        # Create synthesis prompt
        synthesis_prompt = f"""
        You are the AI Coordinator for StadiumVerse AI managing FIFA World Cup 2026 stadium operations.
        
        Current Stadium State:
        - Total Fans: {stadium_state['fans'].get('total', 0)}
        - Average Stress Level: {stadium_state['fans'].get('avg_stress', 0):.1f}%
        - Average Excitement: {stadium_state['fans'].get('avg_excitement', 0):.1f}%
        - Available Volunteers: {stadium_state['volunteers'].get('available', 0)}
        - Active Emergencies: {stadium_state['emergencies'].get('active_count', 0)}
        
        Agent Insights Summary:
        """
        
        for agent_name, insights in agent_insights.items():
            if insights:
                synthesis_prompt += f"\n{agent_name.title()} Agent: {len(insights)} insights"
                for insight in insights[:3]:  # Top 3 insights per agent
                    synthesis_prompt += f"\n  - {insight.get('title', 'Unnamed insight')}"
        
        synthesis_prompt += """
        
        Based on this information, generate 3-5 high-level strategic insights that:
        1. Identify the most critical issues requiring immediate attention
        2. Highlight positive trends and successful operations
        3. Predict potential problems in the next 30 minutes
        4. Recommend specific coordinated actions
        5. Provide natural language explanations with confidence scores
        
        Format each insight as:
        PRIORITY: [1-5]
        TITLE: [Brief title]
        DESCRIPTION: [Natural language explanation with specific recommendations]
        CONFIDENCE: [0.0-1.0]
        """
        
        try:
            response = await self.openai_client.generate_completion(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": synthesis_prompt}
                ],
                temperature=0.3  # Lower temperature for more consistent insights
            )
            
            # Parse LLM response into structured insights
            synthesized_insights = self._parse_llm_insights(response)
            
            return synthesized_insights
            
        except Exception as e:
            logger.error(f"Error synthesizing insights with LLM: {e}")
            
            # Fallback: Create basic synthesis without LLM
            return self._create_fallback_insights(stadium_state, agent_insights)
    
    def _parse_llm_insights(self, llm_response: str) -> List[Dict[str, Any]]:
        """Parse LLM response into structured insights"""
        insights = []
        
        # Split response into individual insights
        lines = llm_response.split('\n')
        current_insight = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('PRIORITY:'):
                if current_insight:
                    insights.append(current_insight)
                current_insight = {
                    "type": "synthesis",
                    "priority": int(line.split(':')[1].strip()),
                    "agent": "coordinator"
                }
            elif line.startswith('TITLE:'):
                current_insight["title"] = line.split(':', 1)[1].strip()
            elif line.startswith('DESCRIPTION:'):
                current_insight["description"] = line.split(':', 1)[1].strip()
            elif line.startswith('CONFIDENCE:'):
                current_insight["confidence"] = float(line.split(':')[1].strip())
        
        # Add last insight
        if current_insight:
            insights.append(current_insight)
        
        return insights
    
    def _create_fallback_insights(self, stadium_state: Dict[str, Any], agent_insights: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        """Create fallback insights without LLM"""
        fallback_insights = []
        
        fan_stats = stadium_state.get("fans", {})
        volunteer_stats = stadium_state.get("volunteers", {})
        
        # High stress alert
        if fan_stats.get("avg_stress", 0) > 70:
            fallback_insights.append({
                "type": "synthesis",
                "priority": 4,
                "title": "Critical: High Overall Crowd Stress",
                "description": f"Stadium-wide stress levels are at {fan_stats.get('avg_stress', 0):.1f}%. Immediate intervention required through volunteer deployment and crowd management.",
                "confidence": 0.9,
                "agent": "coordinator"
            })
        
        # Volunteer utilization
        if volunteer_stats.get("utilization", 0) > 80:
            fallback_insights.append({
                "type": "synthesis",
                "priority": 3,
                "title": "High Volunteer Utilization",
                "description": f"Volunteers are {volunteer_stats.get('utilization', 0):.1f}% utilized. Consider bringing additional volunteers on duty.",
                "confidence": 0.8,
                "agent": "coordinator"
            })
        
        # Positive insight
        if fan_stats.get("avg_excitement", 0) > 70:
            fallback_insights.append({
                "type": "synthesis",
                "priority": 2,
                "title": "Positive: High Fan Engagement",
                "description": f"Fan excitement levels are at {fan_stats.get('avg_excitement', 0):.1f}%. Great atmosphere detected - maintain current service levels.",
                "confidence": 0.7,
                "agent": "coordinator"
            })
        
        return fallback_insights
    
    async def _generate_recommendations(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on insights"""
        recommendations = []
        
        # Sort insights by priority
        high_priority_insights = [i for i in insights if i.get("priority", 0) >= 4]
        
        for insight in high_priority_insights:
            # Generate specific recommendations based on insight type and content
            if "stress" in insight.get("title", "").lower():
                recommendations.append({
                    "type": "recommendation",
                    "priority": 4,
                    "title": "Deploy Additional Navigation Support",
                    "description": "Deploy 3-5 volunteers to high-traffic areas. Open Gate D as emergency exit. Activate digital signage with crowd flow directions.",
                    "confidence": 0.8,
                    "agent": "coordinator",
                    "estimated_impact": "Reduce crowd stress by 15-25%",
                    "implementation_time": "5-10 minutes",
                    "resources_needed": ["5 volunteers", "Digital signage access", "Gate D activation"]
                })
            
            elif "medical" in insight.get("title", "").lower():
                recommendations.append({
                    "type": "recommendation", 
                    "priority": 5,
                    "title": "Activate Emergency Medical Protocol",
                    "description": "Position 2 additional medical teams at North and South plazas. Pre-position wheelchairs at key locations. Alert nearby hospitals.",
                    "confidence": 0.9,
                    "agent": "coordinator",
                    "estimated_impact": "Reduce emergency response time by 40%",
                    "implementation_time": "3-5 minutes", 
                    "resources_needed": ["2 medical teams", "4 wheelchairs", "Hospital coordination"]
                })
            
            elif "volunteer" in insight.get("title", "").lower():
                recommendations.append({
                    "type": "recommendation",
                    "priority": 3,
                    "title": "Optimize Volunteer Deployment",
                    "description": "Call in 5 backup volunteers. Redistribute current volunteers based on crowd density heatmap. Extend break schedules by 15 minutes.",
                    "confidence": 0.7,
                    "agent": "coordinator", 
                    "estimated_impact": "Improve volunteer efficiency by 20%",
                    "implementation_time": "10-15 minutes",
                    "resources_needed": ["5 backup volunteers", "Updated deployment schedule"]
                })
        
        return recommendations
    
    async def _save_insights(self, insights: List[Dict[str, Any]]):
        """Save insights to database"""
        async with AsyncSessionLocal() as session:
            for insight_data in insights:
                insight = AIInsight(
                    insight_type=insight_data.get("type", "general"),
                    title=insight_data.get("title", "Unnamed insight"),
                    description=insight_data.get("description", ""),
                    confidence_score=insight_data.get("confidence", 0.5),
                    priority=insight_data.get("priority", 3),
                    generated_by=f"coordinator_agent_{insight_data.get('agent', 'unknown')}",
                    valid_until=datetime.utcnow() + timedelta(minutes=30),
                    status="active"
                )
                
                # Add additional data
                if "estimated_impact" in insight_data:
                    insight.recommended_actions = {
                        "estimated_impact": insight_data["estimated_impact"],
                        "implementation_time": insight_data.get("implementation_time"),
                        "resources_needed": insight_data.get("resources_needed", [])
                    }
                
                session.add(insight)
            
            await session.commit()
    
    async def coordinate_emergency_response(self, emergency_id: str) -> Dict[str, Any]:
        """Coordinate emergency response across all agents"""
        try:
            async with AsyncSessionLocal() as session:
                # Get emergency details
                emergency_result = await session.execute(
                    select(Emergency).where(Emergency.id == emergency_id)
                )
                emergency = emergency_result.scalar_one_or_none()
                
                if not emergency:
                    return {"error": "Emergency not found"}
                
                # Activate emergency agent for primary response
                emergency_plan = await self.agents["emergency"].handle_emergency(emergency.to_dict())
                
                # Coordinate with other relevant agents
                coordination_tasks = []
                
                # Medical coordination for medical emergencies
                if emergency.emergency_type == "medical":
                    coordination_tasks.append(
                        self.agents["medical"].coordinate_emergency_medical_response(emergency.to_dict())
                    )
                
                # Security coordination for all emergencies
                coordination_tasks.append(
                    self.agents["security"].coordinate_emergency_security_response(emergency.to_dict())
                )
                
                # Volunteer coordination for resource allocation
                coordination_tasks.append(
                    self.agents["volunteer"].coordinate_emergency_volunteers(emergency.to_dict())
                )
                
                # Execute coordination tasks
                coordination_results = await asyncio.gather(*coordination_tasks, return_exceptions=True)
                
                # Compile comprehensive response plan
                response_plan = {
                    "emergency_id": emergency_id,
                    "primary_plan": emergency_plan,
                    "coordination_results": [
                        result for result in coordination_results 
                        if not isinstance(result, Exception)
                    ],
                    "estimated_response_time": emergency_plan.get("estimated_response_time", "5-10 minutes"),
                    "resources_deployed": [],
                    "next_actions": [],
                    "success_probability": 0.85
                }
                
                # Update emergency status
                emergency.status = "response_coordinated"
                emergency.response_plan = str(response_plan)
                await session.commit()
                
                return response_plan
                
        except Exception as e:
            logger.error(f"Error coordinating emergency response: {e}")
            return {"error": str(e)}
    
    async def run_what_if_scenario(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Run what-if scenario analysis"""
        try:
            scenario_type = scenario.get("type")
            scenario_params = scenario.get("parameters", {})
            
            # Get current stadium state for baseline
            current_state = await self._gather_stadium_state()
            
            # Simulate scenario impact
            predicted_impact = await self._simulate_scenario_impact(scenario_type, scenario_params, current_state)
            
            # Generate agent responses to scenario
            agent_responses = {}
            for agent_name, agent in self.agents.items():
                if hasattr(agent, 'analyze_scenario'):
                    response = await agent.analyze_scenario(scenario)
                    agent_responses[agent_name] = response
            
            # Synthesize overall scenario outcome
            scenario_result = {
                "scenario": scenario,
                "current_state": current_state,
                "predicted_impact": predicted_impact,
                "agent_responses": agent_responses,
                "overall_assessment": await self._assess_scenario_outcome(predicted_impact, agent_responses),
                "recommendations": await self._generate_scenario_recommendations(predicted_impact),
                "confidence_score": 0.8,
                "simulation_time": datetime.utcnow().isoformat()
            }
            
            return scenario_result
            
        except Exception as e:
            logger.error(f"Error running what-if scenario: {e}")
            return {"error": str(e)}
    
    async def _simulate_scenario_impact(self, scenario_type: str, params: Dict[str, Any], current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate the impact of a scenario on stadium operations"""
        
        fan_stats = current_state.get("fans", {})
        base_stress = fan_stats.get("avg_stress", 50)
        base_risk = fan_stats.get("avg_risk", 30)
        
        impact = {
            "crowd_impact": {},
            "operational_impact": {},
            "resource_impact": {},
            "timeline": []
        }
        
        if scenario_type == "heavy_rain":
            impact["crowd_impact"] = {
                "stress_change": +25,
                "movement_speed_change": +20,  # People move faster to find shelter
                "queue_tolerance_change": -30
            }
            impact["operational_impact"] = {
                "concession_demand": -40,  # Less outdoor food sales
                "restroom_demand": +60,    # People seek shelter
                "medical_demand": +15      # Slips and falls
            }
            impact["timeline"] = [
                {"time": "0 min", "event": "Rain starts, fans seek shelter"},
                {"time": "5 min", "event": "Queue congestion at covered areas"},
                {"time": "15 min", "event": "Potential crowd crush at entrances"},
                {"time": "30 min", "event": "Stabilization if shelters adequate"}
            ]
        
        elif scenario_type == "gate_closure":
            gate = params.get("gate", "A")
            impact["crowd_impact"] = {
                "stress_change": +20,
                "crowd_redistribution": f"18% of fans reroute to Gate C, expected congestion in 7 minutes"
            }
            impact["operational_impact"] = {
                "volunteer_demand": +5,     # Need crowd control
                "security_demand": +3,     # Gate area management
                "exit_capacity": -15       # Reduced exit options
            }
        
        elif scenario_type == "medical_emergency":
            impact["crowd_impact"] = {
                "stress_change": +30,
                "crowd_avoidance_radius": 50  # meters around incident
            }
            impact["operational_impact"] = {
                "medical_response_time": "3-5 minutes",
                "area_evacuation_needed": True,
                "volunteer_demand": +8
            }
        
        return impact
    
    async def _assess_scenario_outcome(self, predicted_impact: Dict[str, Any], agent_responses: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall scenario outcome"""
        
        # Calculate risk score based on predicted impacts
        risk_factors = []
        
        crowd_impact = predicted_impact.get("crowd_impact", {})
        if crowd_impact.get("stress_change", 0) > 20:
            risk_factors.append("high_stress_increase")
        
        operational_impact = predicted_impact.get("operational_impact", {})
        if operational_impact.get("medical_demand", 0) > 20:
            risk_factors.append("medical_overload")
        
        # Assess agent preparedness
        prepared_agents = sum(1 for response in agent_responses.values() 
                            if response.get("readiness_score", 0) > 0.7)
        
        overall_risk = len(risk_factors) / max(1, len(predicted_impact.keys()))
        overall_preparedness = prepared_agents / len(agent_responses)
        
        return {
            "overall_risk_score": overall_risk,
            "preparedness_score": overall_preparedness,
            "critical_factors": risk_factors,
            "success_probability": max(0.1, overall_preparedness - (overall_risk * 0.5)),
            "recommended_action": "implement" if overall_preparedness > 0.6 else "prepare_more"
        }
    
    async def _generate_scenario_recommendations(self, predicted_impact: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on scenario impact"""
        recommendations = []
        
        crowd_impact = predicted_impact.get("crowd_impact", {})
        operational_impact = predicted_impact.get("operational_impact", {})
        
        if crowd_impact.get("stress_change", 0) > 20:
            recommendations.append("Deploy additional volunteers for crowd management")
            recommendations.append("Activate emergency communication protocols")
        
        if operational_impact.get("medical_demand", 0) > 15:
            recommendations.append("Pre-position medical teams at high-risk areas")
            recommendations.append("Prepare emergency evacuation routes")
        
        if operational_impact.get("volunteer_demand", 0) > 5:
            recommendations.append("Call in backup volunteer staff")
            recommendations.append("Redistribute current volunteer assignments")
        
        return recommendations
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get coordinator agent performance metrics"""
        return {
            "insights_generated": self.insights_generated,
            "recommendations_implemented": self.recommendations_implemented,
            "accuracy_score": self.accuracy_score,
            "active_agents": len([a for a in self.agents.values() if getattr(a, 'is_active', True)]),
            "total_agents": len(self.agents),
            "system_health": "operational"
        }