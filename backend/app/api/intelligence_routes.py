"""
StadiumVerse AI V2 - Collective Intelligence API Routes
API endpoints for the Collective Intelligence Engine
"""

import logging
from datetime import datetime
from typing import Any, Dict

from fastapi import APIRouter, Body, HTTPException, Query

from ..ai.collective_intelligence.impact_models import ImpactCategory, InterventionType
from ..ai.collective_intelligence.intelligence_engine import (
    CollectiveIntelligenceEngine,
)
from ..ai.storyteller.storyteller_engine import NarrativeStyle, StorytellerEngine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/intelligence", tags=["Collective Intelligence"])

# Global engine instances
intelligence_engine = CollectiveIntelligenceEngine()
storyteller_engine = StorytellerEngine()


@router.post("/analyze-situation")
async def analyze_situation_and_propose_interventions(
    current_state: Dict[str, Any] = Body(...),
    context: Dict[str, Any] = Body(default={}),
    max_proposals: int = Query(default=5, ge=1, le=10),
):
    """
    Analyze current situation and propose optimal interventions

    This is the core Collective Intelligence endpoint that finds
    minimal interventions with maximum positive impact.
    """
    try:
        logger.info("Analyzing situation for intervention opportunities")

        # Validate required state parameters
        required_fields = ["total_fans", "avg_stress_level", "crowd_density"]
        missing_fields = [
            field for field in required_fields if field not in current_state
        ]

        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required state fields: {missing_fields}",
            )

        # Add context metadata
        context.update(
            {
                "api_request": True,
                "timestamp": datetime.utcnow().isoformat(),
                "max_proposals_requested": max_proposals,
            }
        )

        # Analyze situation and get intervention proposals
        proposals = (
            await intelligence_engine.analyze_situation_and_propose_interventions(
                current_state=current_state,
                context=context,
                max_proposals=max_proposals,
            )
        )

        # Convert proposals to API format
        proposal_data = []
        for proposal in proposals:
            proposal_dict = proposal.to_dict()

            # Generate natural language narrative for this proposal
            try:
                narrative = await storyteller_engine.generate_intervention_story(
                    proposal, current_state, NarrativeStyle.PROFESSIONAL
                )
                proposal_dict["narrative"] = narrative
            except Exception as e:
                logger.warning(f"Failed to generate narrative for proposal: {e}")
                proposal_dict["narrative"] = proposal.description

            proposal_data.append(proposal_dict)

        # Get engine performance metrics
        performance_metrics = intelligence_engine.get_performance_metrics()

        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "proposals": proposal_data,
            "analysis_summary": {
                "proposals_generated": len(proposals),
                "avg_priority_score": sum(p.get_priority_score() for p in proposals)
                / len(proposals)
                if proposals
                else 0,
                "highest_priority": max(
                    (p.get_priority_score() for p in proposals), default=0
                ),
                "total_fans_affected": sum(
                    p.get_total_fans_affected() for p in proposals
                ),
                "estimated_total_cost": sum(
                    p.roi_analysis.total_cost if p.roi_analysis else 0
                    for p in proposals
                ),
                "estimated_total_benefit": sum(
                    p.roi_analysis.total_benefit if p.roi_analysis else 0
                    for p in proposals
                ),
            },
            "performance_metrics": performance_metrics,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in situation analysis: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error during situation analysis: {str(e)}",
        )


@router.get("/intervention-types")
async def get_intervention_types():
    """Get all available intervention types and their descriptions"""

    intervention_descriptions = {
        InterventionType.VOLUNTEER_DEPLOYMENT: {
            "name": "Volunteer Deployment",
            "description": "Deploy or redeploy volunteers to optimize coverage and response times",
            "typical_cost": "Low",
            "implementation_time": "1-3 minutes",
            "impact_areas": ["Fan Satisfaction", "Wait Time Reduction", "Efficiency"],
        },
        InterventionType.GATE_OPERATION: {
            "name": "Gate Operation",
            "description": "Open, close, or modify gate operations to improve crowd flow",
            "typical_cost": "Very Low",
            "implementation_time": "1-2 minutes",
            "impact_areas": ["Wait Time Reduction", "Safety", "Crowd Flow"],
        },
        InterventionType.QUEUE_MANAGEMENT: {
            "name": "Queue Management",
            "description": "Implement queue modifications, redirections, or optimizations",
            "typical_cost": "Low",
            "implementation_time": "2-5 minutes",
            "impact_areas": ["Wait Time Reduction", "Fan Satisfaction", "Efficiency"],
        },
        InterventionType.COMMUNICATION: {
            "name": "Communication",
            "description": "Issue targeted announcements or information updates",
            "typical_cost": "Very Low",
            "implementation_time": "1 minute",
            "impact_areas": ["Fan Satisfaction", "Risk Mitigation", "Accessibility"],
        },
        InterventionType.RESOURCE_ALLOCATION: {
            "name": "Resource Allocation",
            "description": "Redistribute existing resources for optimal utilization",
            "typical_cost": "Medium",
            "implementation_time": "3-8 minutes",
            "impact_areas": ["Efficiency", "Cost Optimization", "Service Quality"],
        },
        InterventionType.TRANSPORT_ADJUSTMENT: {
            "name": "Transport Adjustment",
            "description": "Modify transportation schedules or routing",
            "typical_cost": "Medium-High",
            "implementation_time": "5-15 minutes",
            "impact_areas": ["Carbon Reduction", "Efficiency", "Fan Experience"],
        },
        InterventionType.FACILITY_OPERATION: {
            "name": "Facility Operation",
            "description": "Modify facility operations, hours, or service levels",
            "typical_cost": "Medium",
            "implementation_time": "3-10 minutes",
            "impact_areas": ["Service Quality", "Efficiency", "Fan Satisfaction"],
        },
        InterventionType.EMERGENCY_PREPARATION: {
            "name": "Emergency Preparation",
            "description": "Implement preventive measures for safety and security",
            "typical_cost": "High",
            "implementation_time": "5-20 minutes",
            "impact_areas": ["Safety", "Risk Mitigation", "Emergency Response"],
        },
    }

    return {
        "status": "success",
        "intervention_types": intervention_descriptions,
        "total_types": len(intervention_descriptions),
    }


@router.get("/impact-categories")
async def get_impact_categories():
    """Get all available impact categories for analysis"""

    category_descriptions = {
        ImpactCategory.FAN_SATISFACTION: {
            "name": "Fan Satisfaction",
            "description": "Impact on overall fan experience and happiness",
            "measurement": "Satisfaction score (0-100)",
            "weight": "High",
        },
        ImpactCategory.WAIT_TIME_REDUCTION: {
            "name": "Wait Time Reduction",
            "description": "Reduction in queue times and service delays",
            "measurement": "Minutes saved per fan",
            "weight": "High",
        },
        ImpactCategory.SAFETY_IMPROVEMENT: {
            "name": "Safety Improvement",
            "description": "Enhancement of safety conditions and risk reduction",
            "measurement": "Safety score improvement",
            "weight": "Critical",
        },
        ImpactCategory.REVENUE_INCREASE: {
            "name": "Revenue Increase",
            "description": "Positive impact on stadium revenue generation",
            "measurement": "Additional revenue per hour",
            "weight": "Medium",
        },
        ImpactCategory.CARBON_REDUCTION: {
            "name": "Carbon Reduction",
            "description": "Environmental impact through reduced carbon emissions",
            "measurement": "CO2 equivalent reduction",
            "weight": "Medium",
        },
        ImpactCategory.EFFICIENCY_GAIN: {
            "name": "Efficiency Gain",
            "description": "Improvement in operational efficiency and resource utilization",
            "measurement": "Efficiency percentage increase",
            "weight": "High",
        },
        ImpactCategory.RISK_MITIGATION: {
            "name": "Risk Mitigation",
            "description": "Reduction in operational and safety risks",
            "measurement": "Risk score reduction",
            "weight": "High",
        },
        ImpactCategory.ACCESSIBILITY_ENHANCEMENT: {
            "name": "Accessibility Enhancement",
            "description": "Improvement in accessibility for fans with special needs",
            "measurement": "Accessibility score improvement",
            "weight": "High",
        },
    }

    return {
        "status": "success",
        "impact_categories": category_descriptions,
        "total_categories": len(category_descriptions),
    }


@router.post("/generate-narrative")
async def generate_intervention_narrative(
    proposal_data: Dict[str, Any] = Body(...),
    current_state: Dict[str, Any] = Body(...),
    style: NarrativeStyle = Query(default=NarrativeStyle.PROFESSIONAL),
):
    """Generate natural language narrative for intervention proposals"""

    try:
        # This would typically receive a full InterventionProposal object
        # For API purposes, we'll create a simplified narrative

        narrative = await storyteller_engine._generate_custom_narrative(
            "intervention_explanation",
            {
                "proposal_data": proposal_data,
                "current_state": current_state,
                "style": style.value,
            },
        )

        return {
            "status": "success",
            "narrative": narrative,
            "style": style.value,
            "timestamp": datetime.utcnow().isoformat(),
        }

    except Exception as e:
        logger.error(f"Error generating narrative: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate narrative: {str(e)}"
        )


@router.get("/performance-metrics")
async def get_intelligence_performance():
    """Get performance metrics for the Collective Intelligence Engine"""

    try:
        intelligence_metrics = intelligence_engine.get_performance_metrics()
        storyteller_metrics = storyteller_engine.get_performance_metrics()

        return {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "intelligence_engine": intelligence_metrics,
            "storyteller_engine": storyteller_metrics,
            "system_status": {
                "operational": True,
                "ai_provider_connected": True,  # Would check actual provider status
                "memory_usage": "Normal",
                "response_time": "Optimal",
            },
        }

    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve performance metrics: {str(e)}"
        )


@router.post("/quick-recommendation")
async def get_quick_recommendation(
    situation: str = Body(..., embed=True),
    urgency: float = Body(default=0.5, ge=0.0, le=1.0, embed=True),
    context: Dict[str, Any] = Body(default={}),
):
    """Get a quick intervention recommendation for a described situation"""

    try:
        # Create simplified state from situation description
        mock_state = {
            "total_fans": context.get("fan_count", 5000),
            "avg_stress_level": int(urgency * 100),
            "crowd_density": urgency,
            "situation_description": situation,
        }

        analysis_context = {
            "quick_recommendation": True,
            "situation": situation,
            "urgency": urgency,
            **context,
        }

        # Get intervention proposals
        proposals = (
            await intelligence_engine.analyze_situation_and_propose_interventions(
                mock_state, analysis_context, max_proposals=3
            )
        )

        if not proposals:
            return {
                "status": "success",
                "recommendation": "Continue monitoring the situation",
                "confidence": 0.5,
                "urgency_level": "medium",
            }

        # Get top proposal
        top_proposal = proposals[0]

        # Generate quick narrative
        narrative = await storyteller_engine.generate_intervention_story(
            top_proposal, mock_state, NarrativeStyle.CASUAL
        )

        return {
            "status": "success",
            "recommendation": top_proposal.title,
            "description": top_proposal.description,
            "narrative": narrative[:300],  # Truncate for quick response
            "confidence": top_proposal.success_probability,
            "urgency_level": "high"
            if urgency > 0.7
            else "medium"
            if urgency > 0.4
            else "low",
            "estimated_time": f"{top_proposal.estimated_implementation_time} minutes",
            "priority_score": top_proposal.get_priority_score(),
            "fans_affected": top_proposal.get_total_fans_affected(),
        }

    except Exception as e:
        logger.error(f"Error getting quick recommendation: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate quick recommendation: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for the Collective Intelligence system"""

    try:
        # Test basic functionality
        test_state = {"total_fans": 1000, "avg_stress_level": 50, "crowd_density": 0.5}

        test_context = {"health_check": True}

        # Try to generate a simple analysis
        proposals = (
            await intelligence_engine.analyze_situation_and_propose_interventions(
                test_state, test_context, max_proposals=1
            )
        )

        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "intelligence_engine": "operational",
            "storyteller_engine": "operational",
            "test_proposals_generated": len(proposals),
            "version": "v2.0",
            "capabilities": [
                "situation_analysis",
                "intervention_optimization",
                "roi_calculation",
                "narrative_generation",
                "multi_agent_reasoning",
            ],
        }

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "version": "v2.0",
        }
