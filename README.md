# StadiumVerse AI V2
## "The Living Brain of the Stadium"
### AI Native Stadium Intelligence Platform

### Vision
An autonomous stadium intelligence platform where the stadium becomes a living brain that continuously observes, predicts, reasons, debates, learns, and adapts. Every entity in the stadium - fans, volunteers, gates, shops, transport nodes - has its own AI Digital Twin with persistent memory and personality.

### Features
- 🧠 Living Stadium Brain that continuously observes, reasons, and adapts
- 🤖 AI Digital Twins for every fan, volunteer, gate, shop, and transport node
- 💭 AI Debate Mode where agents reason and argue before decisions
- 🔮 Future Branch Engine showing Best/Most Likely/Worst scenarios
- ⏰ Time Travel Mode with timeline slider (+5min to +30min predictions)
- 🎯 Collective Intelligence finding minimal interventions with maximum impact
- 📚 Persistent Digital Twin Memory across all stadium visits
- 🎭 Advanced Personality Engine for unique, realistic fan personas
- 🗣️ Voice AI supporting 9 languages with natural conversations
- 📖 AI Storyteller generating natural language narratives
- 🎮 Enhanced simulation scenarios (16+ emergency types)
- 🖥️ Premium FIFA-quality UI with glassmorphism and 3D effects
- 🔍 Explainable AI showing reasoning behind every recommendation
- 🎬 Judge Mode for automatic demonstration sequences

### Core Innovation
The stadium operates as a **Living Brain** where AI Digital Twins maintain persistent memory, debate decisions through multi-agent reasoning, and generate minimal interventions for maximum positive impact.

### Tech Stack
**Frontend**: React, TypeScript, Vite, TailwindCSS, Framer Motion, React Flow, Leaflet, Recharts
**Backend**: FastAPI, Python, WebSockets, Redis, PostgreSQL, SQLAlchemy
**AI**: Local Ollama (qwen2.5-coder:3b), Multi-Agent Reasoning, Persistent Memory
**Infrastructure**: Docker, Nginx, Offline-First Architecture

### Quick Start
```bash
# Clone the repository
git clone <repo-url>
cd stadiumverse-ai

# Start Ollama (required for offline AI)
ollama serve
ollama pull qwen2.5-coder:3b

# Start with Docker
docker-compose up -d

# Or run locally
cd backend && pip install -r requirements.txt && uvicorn main:app --reload
cd frontend && npm install && npm run dev
```

### Offline-First AI
StadiumVerse AI V2 runs completely offline using local Ollama. No external API keys required. The Living Brain operates independently without internet connectivity, ensuring data privacy and operational reliability.

### Architecture
- **Living Brain Engine**: Multi-agent AI system with persistent memory
- **Digital Twin Network**: Individual AI twins for every stadium entity  
- **Debate Chamber**: Agents reason and argue before decisions
- **Future Simulator**: Multiple timeline predictions with confidence scores
- **Collective Intelligence**: Minimal intervention with maximum impact analysis
- **Memory Palace**: Long-term learning and pattern recognition

### Users
1. Fans - Personalized navigation and recommendations
2. Stadium Operators - AI-driven operational insights
3. Volunteers - Smart task assignment and coordination
4. Security Teams - Predictive threat assessment
5. Medical Teams - Health risk monitoring and response
6. Transport Operators - Crowd flow optimization
7. Sustainability Managers - Carbon footprint optimization

### Demo Scenarios
- Real-time crowd simulation with 100 digital fans
- Emergency response prediction and coordination
- Weather impact on crowd behavior
- Transport optimization during peak times
- Volunteer deployment optimization
- Accessibility support automation

Built for FIFA World Cup 2026 🏆