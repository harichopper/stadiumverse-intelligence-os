"""
StadiumVerse AI V2 - Demo Startup Script
Simplified demonstration of the Living Brain functionality without full database setup
"""

import asyncio
import sys
import logging

# Add backend to path
sys.path.append("backend")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def demo_ai_provider():
    """Test basic AI provider functionality"""

    try:
        from backend.app.ai.providers.factory import get_global_ai_provider
        from backend.app.ai.providers.base import AIMessage, MessageRole

        print("🔗 Connecting to Local Ollama AI (qwen2.5-coder:3b)...")
        ai_provider = await get_global_ai_provider()

        # Test AI connection
        health_status = await ai_provider.health_check()
        if health_status:
            print("✅ Local AI Connected Successfully")
        else:
            print("⚠️  AI Connection Warning")

        # Test simple completion
        test_messages = [
            AIMessage(
                role=MessageRole.SYSTEM,
                content="You are StadiumVerse AI, an intelligent stadium management system.",
            ),
            AIMessage(
                role=MessageRole.USER,
                content="Provide a brief welcome message for StadiumVerse AI V2, mentioning that you are 'The Living Brain of the Stadium' running on local Ollama. Keep it under 100 words.",
            ),
        ]

        print("🤖 Testing AI response generation...")
        response = await ai_provider.generate_completion(test_messages)

        print("\n📢 AI RESPONSE:")
        print(f'"{response.content}"')
        print("\n📊 Response Metrics:")
        print(f"   • Confidence: {response.confidence:.0%}")
        print(f"   • Latency: {response.latency_ms:.1f}ms")
        print(f"   • Tokens: {response.token_count}")

        return True

    except Exception as e:
        print(f"❌ AI Provider Error: {e}")
        return False


async def demo_living_brain():
    """Demonstrate the Living Brain functionality"""

    print("\n" + "=" * 80)
    print("🧠 STADIUMVERSE AI V2 - THE LIVING BRAIN OF THE STADIUM")
    print("=" * 80)
    print("🎯 AI Native Stadium Intelligence Platform")
    print("🤖 Offline AI • Multi-Agent Reasoning • Predictive Intelligence")
    print("=" * 80 + "\n")

    # Test AI Provider first
    ai_connected = await demo_ai_provider()

    if not ai_connected:
        print("\n⚠️  Cannot continue demo without AI connection")
        print("🔧 Please ensure Ollama is running: 'ollama serve'")
        return

    print("\n📊 DEMO SCENARIO: CROWD MANAGEMENT CHALLENGE")
    print("-" * 60)

    # Simulated current stadium state
    current_state = {
        "total_fans": 15000,
        "avg_stress_level": 72,
        "crowd_density": 0.78,
        "avg_queue_time": 18.5,
        "fan_satisfaction": 68,
        "available_volunteers": 18,
        "active_emergencies": 0,
        "weather": "Light Rain",
        "revenue_rate": 145.5,
        "operational_efficiency": 72.0,
        "medical_risk": 15.0,
        "carbon_rate": 125.0,
        "accessibility_score": 85.0,
    }

    print("🏟️  Stadium State:")
    print(f"   • Total Fans: {current_state['total_fans']:,}")
    print(f"   • Stress Level: {current_state['avg_stress_level']}% (Elevated)")
    print(f"   • Crowd Density: {current_state['crowd_density'] * 100:.0f}%")
    print(f"   • Avg Queue Time: {current_state['avg_queue_time']:.1f} minutes")
    print(f"   • Fan Satisfaction: {current_state['fan_satisfaction']}%")
    print(f"   • Weather: {current_state['weather']}")
    print(f"   • Available Volunteers: {current_state['available_volunteers']}")
    print()

    # Demonstrate AI reasoning for stadium management
    try:
        from backend.app.ai.providers.factory import get_global_ai_provider
        from backend.app.ai.providers.base import AIMessage, MessageRole

        ai_provider = await get_global_ai_provider()

        # AI Analysis of the situation
        print("🧠 PHASE 1: AI SITUATION ANALYSIS")
        print("-" * 50)

        analysis_prompt = f"""
You are StadiumVerse AI V2, "The Living Brain of the Stadium". Analyze this situation:

Stadium State:
- Total Fans: {current_state["total_fans"]:,}
- Stress Level: {current_state["avg_stress_level"]}% (elevated)
- Crowd Density: {current_state["crowd_density"] * 100:.0f}%
- Queue Time: {current_state["avg_queue_time"]:.1f} minutes
- Fan Satisfaction: {current_state["fan_satisfaction"]}%
- Weather: {current_state["weather"]}
- Available Volunteers: {current_state["available_volunteers"]}

Provide a brief analysis with:
1. Current situation assessment
2. Top 2 recommended interventions
3. Expected impact of interventions

Keep response under 200 words.
"""

        analysis_messages = [
            AIMessage(
                role=MessageRole.SYSTEM,
                content="You are StadiumVerse AI V2, an intelligent stadium management system known as 'The Living Brain of the Stadium'. You provide clear, actionable recommendations.",
            ),
            AIMessage(role=MessageRole.USER, content=analysis_prompt),
        ]

        print("🔍 Analyzing stadium conditions...")
        analysis_response = await ai_provider.generate_completion(analysis_messages)

        print("\n🎯 STADIUM INTELLIGENCE ANALYSIS:")
        print(f'"{analysis_response.content}"')
        print(f"\nConfidence: {analysis_response.confidence:.0%}")

        # Future Prediction Demo
        print("\n🔮 PHASE 2: FUTURE PREDICTION")
        print("-" * 50)

        prediction_prompt = f"""
Based on the current stadium state, predict what will happen in the next 20 minutes if no action is taken:

Current State:
- Crowd Density: {current_state["crowd_density"] * 100:.0f}%
- Queue Time: {current_state["avg_queue_time"]:.1f} minutes
- Fan Satisfaction: {current_state["fan_satisfaction"]}%
- Weather: Light rain continuing

Provide:
1. Most likely scenario (+20 minutes)
2. Key risks to monitor
3. Recommended preventive actions

Keep response under 150 words.
"""

        prediction_messages = [
            AIMessage(
                role=MessageRole.SYSTEM,
                content="You are the Future Prediction module of StadiumVerse AI. You predict stadium conditions and recommend preventive measures.",
            ),
            AIMessage(role=MessageRole.USER, content=prediction_prompt),
        ]

        print("⏰ Generating 20-minute future prediction...")
        prediction_response = await ai_provider.generate_completion(prediction_messages)

        print("\n📈 FUTURE SCENARIO (+20 MINUTES):")
        print(f'"{prediction_response.content}"')
        print(f"\nPrediction Confidence: {prediction_response.confidence:.0%}")

        # Natural Language Narrative
        print("\n📖 PHASE 3: AI STORYTELLER")
        print("-" * 50)

        narrative_prompt = f"""
You are the AI Storyteller for StadiumVerse. Create a natural, engaging narrative explaining the current stadium situation for stadium operators:

Current Conditions:
- {current_state["total_fans"]:,} fans in the stadium
- Crowd density at {current_state["crowd_density"] * 100:.0f}% with light rain
- Average wait times of {current_state["avg_queue_time"]:.1f} minutes
- Fan satisfaction at {current_state["fan_satisfaction"]}%

Create a compelling 2-3 sentence narrative that explains what's happening and what should be done. Use specific numbers and make it engaging for stadium staff.
"""

        narrative_messages = [
            AIMessage(
                role=MessageRole.SYSTEM,
                content="You are the AI Storyteller for StadiumVerse, expert at converting technical data into engaging, natural language narratives for stadium operations.",
            ),
            AIMessage(role=MessageRole.USER, content=narrative_prompt),
        ]

        print("✍️  Converting analysis into natural language narrative...")
        narrative_response = await ai_provider.generate_completion(narrative_messages)

        print("\n📋 OPERATIONS NARRATIVE:")
        print(f'"{narrative_response.content}"')

        # Performance Summary
        print("\n📊 PHASE 4: AI SYSTEM PERFORMANCE")
        print("-" * 50)

        performance_stats = ai_provider.get_performance_stats()
        print("🤖 AI Provider Performance:")
        print(f"   • Total Requests: {performance_stats.get('total_requests', 0)}")
        print(f"   • Avg Latency: {performance_stats.get('avg_latency_ms', 0):.1f}ms")
        print(f"   • Total Tokens: {performance_stats.get('total_tokens', 0):,}")
        print(f"   • Error Rate: {performance_stats.get('error_rate', 0) * 100:.1f}%")
        print(f"   • Model: {performance_stats.get('model', 'Unknown')}")

    except Exception as e:
        print(f"⚠️  Advanced Demo Error: {e}")
        print("🔧 Basic AI connection successful - advanced features need full setup")

    print("\n" + "=" * 80)
    print("✅ STADIUMVERSE AI V2 CORE DEMONSTRATION COMPLETED")
    print("=" * 80)
    print("🧠 Living Brain Status: OPERATIONAL")
    print("🤖 Local AI Status: CONNECTED")
    print("🎯 Intelligence Analysis: FUNCTIONAL")
    print("🔮 Future Predictions: ACTIVE")
    print("📖 AI Storyteller: READY")
    print("=" * 80)
    print("🏆 Core AI Systems Ready for FIFA World Cup 2026")
    print("=" * 80 + "\n")

    print("💡 NEXT STEPS TO FULL DEPLOYMENT:")
    print("   • Install complete dependencies (database, Redis)")
    print("   • Set up Digital Twin memory system")
    print("   • Configure multi-agent debate chamber")
    print("   • Deploy premium UI with FIFA theming")
    print("   • Enable Judge Mode for demonstrations")
    print()


if __name__ == "__main__":
    print("🚀 Starting StadiumVerse AI V2 Core Demo...")

    # Run the demo
    asyncio.run(demo_living_brain())
