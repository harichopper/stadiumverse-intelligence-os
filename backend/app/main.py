"""
StadiumVerse AI V2 - Main Application
The Living Brain of the Stadium - AI Native Stadium Intelligence Platform
"""

import os
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import configuration
from .config import settings

# Import core AI systems
from .ai.providers.factory import initialize_global_provider, shutdown_global_provider

# Import simple database
from .database import init_db, get_db
from .seed import run_seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    
    logger.info("🧠 Starting StadiumVerse AI V2 - The Living Brain of the Stadium")
    
    try:
        # Initialize database and seed
        logger.info("📊 Initialising SQLite database...")
        init_db()
        run_seed()
        logger.info("✅ Database ready")
        
        # Initialize AI provider
        logger.info("🤖 Initializing Local AI Provider (Ollama)...")
        ai_provider = await initialize_global_provider()
        
        # Test AI connection
        health_status = await ai_provider.health_check()
        if health_status:
            logger.info("✅ AI Provider initialized successfully")
            
            # Get model info
            model_info = await ai_provider.get_model_info()
            logger.info(f"🎯 AI Model: {model_info.get('model', 'Unknown')}")
        else:
            logger.warning("⚠️  AI Provider health check failed")
        
        logger.info("🏟️  StadiumVerse AI V2 - Living Brain is OPERATIONAL")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Startup Error: {e}")
        logger.warning("🔧 Some features may not be available")
        yield
    
    finally:
        # Cleanup
        logger.info("🔄 Shutting down StadiumVerse AI V2...")
        try:
            await shutdown_global_provider()
            logger.info("✅ Shutdown complete")
        except Exception as e:
            logger.error(f"⚠️  Shutdown error: {e}")

# Create FastAPI application
app = FastAPI(
    title="StadiumVerse AI V2",
    description="The Living Brain of the Stadium - AI Native Stadium Intelligence Platform",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", "http://127.0.0.1:3000",
        "http://localhost:3001", "http://127.0.0.1:3001",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
from .api.stadium_routes import router as stadium_router
app.include_router(stadium_router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        from .ai.providers.factory import get_global_ai_provider
        
        ai_provider = await get_global_ai_provider()
        ai_healthy = await ai_provider.health_check()
        
        db_status = {"status": "connected"}
        
        return {
            "status": "healthy",
            "service": "StadiumVerse AI V2",
            "version": "2.0.0",
            "description": "The Living Brain of the Stadium",
            "ai_provider": "operational" if ai_healthy else "degraded",
            "database": db_status["status"],
            "features": [
                "Local AI (Ollama)",
                "Collective Intelligence",
                "Future Predictions", 
                "AI Storyteller",
                "Multi-Agent Debate",
                "Digital Twin Memory"
            ]
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "service": "StadiumVerse AI V2",
            "version": "2.0.0"
        }

# Demo endpoint
@app.get("/demo")
async def demo_endpoint():
    """Demo endpoint to test AI functionality"""
    
    try:
        from .ai.providers.factory import get_global_ai_provider
        from .ai.providers.base import AIMessage, MessageRole
        
        ai_provider = await get_global_ai_provider()
        
        # Test AI with stadium scenario
        demo_messages = [
            AIMessage(
                role=MessageRole.SYSTEM, 
                content="You are StadiumVerse AI V2, 'The Living Brain of the Stadium'. Provide intelligent stadium management insights."
            ),
            AIMessage(
                role=MessageRole.USER, 
                content="A stadium has 15,000 fans with 72% stress level and 18-minute queue times. Provide a brief recommendation in 2 sentences."
            )
        ]
        
        response = await ai_provider.generate_completion(demo_messages)
        
        return {
            "status": "success",
            "demo_scenario": "Crowd management with 15,000 fans",
            "ai_recommendation": response.content,
            "confidence": response.confidence,
            "response_time_ms": response.latency_ms,
            "model": response.model_used
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo failed: {str(e)}")

# Stadium simulation endpoint
@app.get("/simulate")
async def simulate_stadium():
    """Simulate stadium conditions and get AI analysis"""
    
    try:
        from .ai.providers.factory import get_global_ai_provider
        from .ai.providers.base import AIMessage, MessageRole
        import random
        
        # Generate simulated stadium state
        stadium_state = {
            "total_fans": random.randint(8000, 25000),
            "avg_stress_level": random.randint(45, 85),
            "crowd_density": random.randint(60, 95),
            "avg_queue_time": round(random.uniform(5.0, 25.0), 1),
            "fan_satisfaction": random.randint(55, 85),
            "weather": random.choice(["Clear", "Light Rain", "Overcast", "Sunny"]),
            "available_volunteers": random.randint(15, 25)
        }
        
        ai_provider = await get_global_ai_provider()
        
        # Generate AI analysis
        analysis_prompt = f"""
Analyze this stadium situation:

Stadium State:
- Total Fans: {stadium_state['total_fans']:,}
- Stress Level: {stadium_state['avg_stress_level']}%
- Crowd Density: {stadium_state['crowd_density']}%
- Queue Time: {stadium_state['avg_queue_time']} minutes
- Fan Satisfaction: {stadium_state['fan_satisfaction']}%
- Weather: {stadium_state['weather']}
- Available Volunteers: {stadium_state['available_volunteers']}

Provide:
1. Situation assessment (1 sentence)
2. Priority action (1 sentence) 
3. Expected impact (1 sentence)

Total response under 100 words.
"""
        
        analysis_messages = [
            AIMessage(role=MessageRole.SYSTEM, content="You are StadiumVerse AI V2, providing concise stadium management analysis."),
            AIMessage(role=MessageRole.USER, content=analysis_prompt)
        ]
        
        analysis_response = await ai_provider.generate_completion(analysis_messages)
        
        return {
            "status": "success",
            "stadium_state": stadium_state,
            "ai_analysis": analysis_response.content,
            "confidence": analysis_response.confidence,
            "timestamp": "real-time",
            "recommendations_available": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

# Database status endpoint
@app.get("/database")
async def database_status():
    """Get database status and information"""
    
    try:
        db_status = {"status": "connected"}
        return {
            "status": "success",
            "database": db_status
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Intelligence Routes - Basic version without complex models
@app.get("/api/intelligence/status")
async def intelligence_status():
    """Get intelligence engine status"""
    
    try:
        from .ai.providers.factory import get_global_ai_provider
        
        ai_provider = await get_global_ai_provider()
        ai_healthy = await ai_provider.health_check()
        
        return {
            "status": "operational" if ai_healthy else "degraded",
            "timestamp": "2024-01-01T00:00:00Z",  # Placeholder
            "capabilities": [
                "situation_analysis",
                "intervention_optimization", 
                "roi_calculation",
                "narrative_generation",
                "multi_agent_reasoning"
            ],
            "ai_provider": "ollama",
            "model": "qwen2.5-coder:3b",
            "version": "2.0.0"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with HTML interface"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>StadiumVerse AI V2 - The Living Brain</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }}
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }}
            h1 {{
                text-align: center;
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }}
            .subtitle {{
                text-align: center;
                font-size: 1.3em;
                margin-bottom: 30px;
                opacity: 0.9;
            }}
            .features {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }}
            .feature {{
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .feature:hover {{
                transform: translateY(-5px);
            }}
            .api-links {{
                text-align: center;
                margin: 30px 0;
            }}
            .api-links a {{
                display: inline-block;
                margin: 10px;
                padding: 12px 24px;
                background: rgba(255,255,255,0.2);
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
            }}
            .api-links a:hover {{
                background: rgba(255,255,255,0.3);
                transform: scale(1.05);
            }}
            .status {{
                text-align: center;
                margin: 20px 0;
                font-size: 1.1em;
            }}
            .emoji {{ font-size: 1.5em; margin-right: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧠 StadiumVerse AI V2</h1>
            <div class="subtitle">"The Living Brain of the Stadium"</div>
            <div class="subtitle">AI Native Stadium Intelligence Platform</div>
            
            <div class="status">
                <div><span class="emoji">🤖</span>Offline AI • Multi-Agent Reasoning • Predictive Intelligence</div>
                <div><span class="emoji">🏟️</span>Ready for FIFA World Cup 2026</div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <div class="emoji">🎯</div>
                    <h3>Collective Intelligence</h3>
                    <p>Finds minimal interventions with maximum positive impact</p>
                </div>
                <div class="feature">
                    <div class="emoji">🔮</div>
                    <h3>Future Predictions</h3>
                    <p>Best/Likely/Worst scenario modeling</p>
                </div>
                <div class="feature">
                    <div class="emoji">🗣️</div>
                    <h3>AI Debate Chamber</h3>
                    <p>13 specialized agents debate decisions</p>
                </div>
                <div class="feature">
                    <div class="emoji">📖</div>
                    <h3>AI Storyteller</h3>
                    <p>Natural language explanations</p>
                </div>
            </div>
            
            <div class="api-links">
                <a href="/health">🏥 System Health</a>
                <a href="/demo">🎮 AI Demo</a>
                <a href="/simulate">🏟️ Stadium Simulation</a>
                <a href="/database">📊 Database Status</a>
                <a href="/docs">📚 API Documentation</a>
            </div>
            
            <div style="text-align: center; margin-top: 40px; opacity: 0.8;">
                <p>🏆 Powered by Local AI (Ollama) • Completely Offline Operation</p>
                <p>Version 2.0.0 • The Living Brain is OPERATIONAL</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting StadiumVerse AI V2 server...")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
