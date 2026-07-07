"""
StadiumVerse AI V2 - Simple Demo
Direct demonstration of AI capabilities without complex imports
"""

import asyncio
import json
import aiohttp
from datetime import datetime

async def test_ollama_connection():
    """Test direct connection to Ollama"""
    
    print("\n" + "="*80)
    print("🧠 STADIUMVERSE AI V2 - THE LIVING BRAIN OF THE STADIUM")
    print("="*80)
    print("🎯 AI Native Stadium Intelligence Platform")
    print("🤖 Offline AI • Multi-Agent Reasoning • Predictive Intelligence")
    print("="*80 + "\n")
    
    print("🔗 Testing Local Ollama Connection...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test if Ollama is running
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get("models", [])
                    
                    print("✅ Ollama is running!")
                    print(f"📦 Available models: {len(models)}")
                    
                    # Check for qwen2.5-coder:3b
                    qwen_model = None
                    for model in models:
                        if "qwen2.5-coder:3b" in model.get("name", ""):
                            qwen_model = model
                            break
                    
                    if qwen_model:
                        print("✅ qwen2.5-coder:3b model found!")
                        print(f"   Model size: {qwen_model.get('size', 0) / (1024**3):.1f} GB")
                        print(f"   Modified: {qwen_model.get('modified', 'Unknown')}")
                        
                        # Now test AI generation
                        await demo_ai_intelligence()
                    else:
                        print("❌ qwen2.5-coder:3b model not found")
                        print("💡 Run: ollama pull qwen2.5-coder:3b")
                else:
                    print(f"❌ Ollama API returned status {response.status}")
                    
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Make sure Ollama is running: 'ollama serve'")

async def demo_ai_intelligence():
    """Demonstrate AI intelligence with stadium scenarios"""
    
    print("\n📊 DEMO SCENARIO: CROWD MANAGEMENT CHALLENGE")
    print("-" * 60)
    
    # Stadium state
    stadium_state = {
        "total_fans": 15000,
        "avg_stress_level": 72,
        "crowd_density": 78,
        "avg_queue_time": 18.5,
        "fan_satisfaction": 68,
        "weather": "Light Rain",
        "available_volunteers": 18
    }
    
    print(f"🏟️  Stadium State:")
    for key, value in stadium_state.items():
        formatted_key = key.replace('_', ' ').title()
        if isinstance(value, (int, float)):
            if 'level' in key or 'satisfaction' in key or 'density' in key:
                print(f"   • {formatted_key}: {value}%")
            elif 'time' in key:
                print(f"   • {formatted_key}: {value} minutes")
            else:
                print(f"   • {formatted_key}: {value:,}")
        else:
            print(f"   • {formatted_key}: {value}")
    
    print("\n🧠 PHASE 1: AI SITUATION ANALYSIS")
    print("-" * 50)
    
    # Test AI analysis
    analysis_prompt = f"""
You are StadiumVerse AI V2, "The Living Brain of the Stadium". Analyze this situation:

Stadium State:
- Total Fans: {stadium_state['total_fans']:,}
- Stress Level: {stadium_state['avg_stress_level']}% (elevated)  
- Crowd Density: {stadium_state['crowd_density']}%
- Queue Time: {stadium_state['avg_queue_time']} minutes
- Fan Satisfaction: {stadium_state['fan_satisfaction']}%
- Weather: {stadium_state['weather']}
- Available Volunteers: {stadium_state['available_volunteers']}

Provide a brief analysis with:
1. Current situation assessment (2 sentences)
2. Top 2 recommended interventions
3. Expected impact

Keep response under 150 words and be specific with numbers.
"""
    
    print("🔍 Analyzing stadium conditions...")
    
    ai_response = await call_ollama_api(
        model="qwen2.5-coder:3b",
        system="You are StadiumVerse AI V2, an intelligent stadium management system known as 'The Living Brain of the Stadium'. You provide clear, actionable recommendations with specific numbers.",
        prompt=analysis_prompt
    )
    
    if ai_response:
        print("\n🎯 STADIUM INTELLIGENCE ANALYSIS:")
        print(f'"{ai_response["response"]}"')
        print(f"\n📊 AI Performance:")
        print(f"   • Response time: {ai_response.get('total_duration', 0) / 1000000:.1f}ms")
        print(f"   • Tokens generated: {ai_response.get('eval_count', 0)}")
        
        # Future prediction
        print("\n🔮 PHASE 2: FUTURE PREDICTION")
        print("-" * 50)
        
        prediction_prompt = f"""
Based on the current stadium state, predict what will happen in the next 20 minutes if no action is taken:

Current Critical Metrics:
- Crowd Density: {stadium_state['crowd_density']}%
- Queue Time: {stadium_state['avg_queue_time']} minutes  
- Fan Satisfaction: {stadium_state['fan_satisfaction']}%
- Weather: Light rain continuing

Provide a specific prediction:
1. Most likely scenario at +20 minutes
2. Key risks to monitor
3. Recommended preventive action

Use specific numbers and timeframes. Keep under 120 words.
"""
        
        print("⏰ Generating 20-minute future prediction...")
        
        prediction_response = await call_ollama_api(
            model="qwen2.5-coder:3b", 
            system="You are the Future Prediction module of StadiumVerse AI. You predict stadium conditions with specific metrics and timeframes.",
            prompt=prediction_prompt
        )
        
        if prediction_response:
            print("\n📈 FUTURE SCENARIO (+20 MINUTES):")
            print(f'"{prediction_response["response"]}"')
            
            # AI Storyteller
            print("\n📖 PHASE 3: AI STORYTELLER")
            print("-" * 50)
            
            narrative_prompt = f"""
You are the AI Storyteller for StadiumVerse. Create an engaging narrative for stadium operators:

Current Situation:
- {stadium_state['total_fans']:,} fans experiencing {stadium_state['crowd_density']}% density
- Average wait times of {stadium_state['avg_queue_time']} minutes with light rain
- Fan satisfaction at {stadium_state['fan_satisfaction']}%

Create a compelling 2-3 sentence narrative that explains what's happening and what should be done. Use specific numbers and make it engaging for stadium operations staff.
"""
            
            print("✍️  Converting analysis into natural language narrative...")
            
            story_response = await call_ollama_api(
                model="qwen2.5-coder:3b",
                system="You are the AI Storyteller for StadiumVerse, expert at converting technical data into engaging, natural language narratives.",
                prompt=narrative_prompt
            )
            
            if story_response:
                print("\n📋 OPERATIONS NARRATIVE:")
                print(f'"{story_response["response"]}"')
                
                # Demonstrate decision making
                print("\n🗣️  PHASE 4: AI DECISION MAKING")
                print("-" * 50)
                
                decision_prompt = f"""
As the Living Brain of the Stadium, you must make a decision:

SITUATION: {stadium_state['avg_queue_time']} minute wait times, {stadium_state['crowd_density']}% density, {stadium_state['fan_satisfaction']}% satisfaction

OPTION A: Deploy 3 additional volunteers to high-traffic areas (Cost: $45/hour, Implementation: 3 minutes)
OPTION B: Open secondary entrance gates (Cost: $20/hour security, Implementation: 5 minutes)  
OPTION C: Issue multilingual announcements about alternative routes (Cost: $5, Implementation: 1 minute)

Choose ONE option and explain:
1. Your choice and why
2. Expected impact on wait times and satisfaction
3. Implementation timeline
4. Success probability

Be decisive and specific with numbers.
"""
                
                print("🎯 Making operational decision...")
                
                decision_response = await call_ollama_api(
                    model="qwen2.5-coder:3b",
                    system="You are the Decision Engine of StadiumVerse AI. You make clear, decisive choices with specific reasoning and impact predictions.",
                    prompt=decision_prompt
                )
                
                if decision_response:
                    print("\n⚡ LIVING BRAIN DECISION:")
                    print(f'"{decision_response["response"]}"')
                    
                    print("\n" + "="*80)
                    print("✅ STADIUMVERSE AI V2 CORE DEMONSTRATION COMPLETED")
                    print("="*80)
                    print("🧠 Living Brain Status: OPERATIONAL")
                    print("🤖 Local AI Status: CONNECTED")
                    print("🎯 Intelligence Analysis: FUNCTIONAL")
                    print("🔮 Future Predictions: ACTIVE")
                    print("📖 AI Storyteller: READY")
                    print("⚡ Decision Engine: OPERATIONAL")
                    print("="*80)
                    print("🏆 Core AI Systems Ready for FIFA World Cup 2026")
                    print("="*80 + "\n")
                    
                    print("💡 STADIUMVERSE AI V2 FEATURES DEMONSTRATED:")
                    print("   ✅ Offline AI processing with Ollama")
                    print("   ✅ Real-time situation analysis")
                    print("   ✅ Future scenario prediction")
                    print("   ✅ Natural language storytelling")
                    print("   ✅ Automated decision making")
                    print("   ✅ Multi-perspective reasoning")
                    print()
                    
                    print("🚀 NEXT STEPS FOR FULL DEPLOYMENT:")
                    print("   • Set up Digital Twin memory system")
                    print("   • Enable multi-agent debate chamber")
                    print("   • Deploy premium FIFA-themed UI")
                    print("   • Configure Judge Mode demonstrations")
                    print("   • Integrate with stadium hardware systems")
                    print()

async def call_ollama_api(model: str, system: str, prompt: str) -> dict:
    """Call Ollama API directly"""
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": model,
                "system": system,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200,
                    "num_ctx": 4096
                }
            }
            
            async with session.post("http://localhost:11434/api/generate", json=payload) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"❌ API Error: {response.status}")
                    return None
                    
    except Exception as e:
        print(f"❌ API Call Error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Starting StadiumVerse AI V2 Simple Demo...")
    asyncio.run(test_ollama_connection())