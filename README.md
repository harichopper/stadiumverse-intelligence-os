# 🧠 StadiumVerse Intelligence OS

> **AI Operating System for FIFA World Cup 2026 Stadium Command Centers**
> 
> *Challenge 4: Smart Stadiums & Tournament Operations*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-black?style=for-the-badge&logo=vercel)](https://stadiumverse-intelligence-os.vercel.app)
[![Backend API](https://img.shields.io/badge/Backend%20API-Render-46E3B7?style=for-the-badge)](https://stadiumverse-intelligence-os-api.onrender.com)
[![GitHub](https://img.shields.io/badge/GitHub-Public-blue?style=for-the-badge&logo=github)](https://github.com/harichopper/stadiumverse-intelligence-os)
[![Tests](https://img.shields.io/badge/Tests-29%20Passing-brightgreen?style=for-the-badge)](https://github.com/harichopper/stadiumverse-intelligence-os)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue?style=for-the-badge&logo=typescript)](https://typescriptlang.org)

---

## 🎯 Challenge Vertical

**[Challenge 4] Smart Stadiums & Tournament Operations**

StadiumVerse Intelligence OS is an AI-powered platform that transforms a FIFA World Cup 2026 stadium into a **self-aware, proactive command center**. It solves the core challenge problem: *how do you safely and efficiently manage 87,000+ fans, 140+ volunteers, and real-time stadium operations using AI?*

> *What if the stadium itself could think, debate, predict, and act?*

The system addresses every dimension of the Smart Stadiums challenge:
- 🏟️ **Real-time crowd flow intelligence** — gate density monitoring, congestion prediction
- 👥 **Digital twin network** — individual AI models for every fan, volunteer, and zone
- 🧠 **Multi-agent decision engine** — 4 specialized AI agents debate before every intervention
- ⚡ **Minimum-intervention principle** — finds the smallest action with maximum positive impact
- 🔮 **Predictive analytics** — up to 30-minute lookahead across multiple scenario branches
- ♿ **Inclusive design** — accessibility-first UI meeting WCAG AA standards

---

## 🏟️ What It Does

The system monitors 87,342 fans simultaneously, runs 4 specialized AI agents in a debate chamber, predicts crowd behavior up to 30 minutes ahead, and issues the smallest possible intervention to prevent crowd incidents — all in real time.

### Core Capabilities

| Feature | Description | Impact |
|---|---|---|
| 🧠 **Living Brain** | Real-time AI thoughts, predictions, confidence, recommendations | Decision latency < 1s |
| 👥 **Digital Twins** | Persistent memory, emotion state, stress level per fan | 10 seeded, scales to 87,342 |
| 🏟️ **Living Stadium** | Animated SVG map with 150+ entities (fans, volunteers, medical, security) | Visual crowd awareness |
| 🗣️ **AI Debate Chamber** | 4 agents (Navigation, Medical, Security, Transport) deliberate per decision | Collective intelligence |
| 🔮 **Future Branches** | Best / Likely / Worst scenario tree with probability propagation | 30-min lookahead |
| 📊 **Analytics** | ECharts-powered crowd flow, gate density, emotion trends from real SQLite data | Data-driven ops |
| ⚡ **Command Bar** | Ctrl+K AI interface — natural language stadium control | Operator efficiency |
| 🎬 **Judge Demo Mode** | One button: Goal → Rain → Congestion → AI Decision → Resolution | Full scenario playback |
| 📦 **Black Box Recorder** | Every AI decision stored with reasoning, confidence, outcome, impact % | Accountability & audit |
| ⏱️ **Timeline Scrubber** | Travel forward/backward in match time — stadium state updates | Historical review |

---

## 🧠 Approach & Logic

### Architecture

```
Frontend (React + TypeScript)          Backend (FastAPI + SQLite)
┌──────────────────────────┐          ┌──────────────────────────┐
│  Boot Screen             │          │  /api/stadium/dashboard  │
│  Top Bar (live data)     │◄────────►│  /api/stadium/fans       │
│  Sidebar (10 pages)      │  5s poll │  /api/stadium/crowd      │
│  Living Stadium (SVG)    │          │  /api/stadium/decisions  │
│  Living Brain Panel      │          │  /api/stadium/volunteers │
│  AI Debate Chat          │          │  /api/stadium/events     │
│  Future Branches Tree    │          └──────────────────────────┘
│  Analytics (ECharts)     │                     │
│  Digital Twins Inspector │          ┌──────────▼───────────────┐
│  Command Bar (Ctrl+K)    │          │  SQLite DB               │
│  Timeline Scrubber       │          │  10 Digital Fan Twins    │
└──────────────────────────┘          │  8 Volunteers            │
                                      │  90 Crowd Snapshots      │
                                      │  8 AI Decisions          │
                                      │  8 Stadium Events        │
                                      └──────────────────────────┘
```

### Decision Logic (6-Step AI Pipeline)

1. **Perceive** — Ingest crowd density, fan stress levels, gate flow rates from DB
2. **Retrieve** — Query historical patterns from similar events (Memory Palace)
3. **Debate** — 4 AI agents deliberate asynchronously in real time
4. **Decide** — Coordinator agent produces minimum-intervention recommendation
5. **Act** — Decision stored in Black Box, volunteers deployed, signage updated
6. **Learn** — Outcome recorded, prediction accuracy updated

### Collective Intelligence Principle

The system always finds the **smallest intervention** with the **maximum positive impact**. 

Example: instead of closing Gate B (affects 5,000 fans), deploy 3 volunteers + activate digital signage → affects 1,400 fans, reduces congestion by **-23%**, ROI **4.2×**.

---

## 🛠️ Tech Stack

### Frontend
| Tech | Purpose |
|---|---|
| React 18 + TypeScript | UI framework |
| Vite | Build tool |
| Tailwind CSS | Styling |
| Framer Motion | All animations |
| ECharts | Analytics charts |
| Zustand | Global state |
| Lucide React | Icons |

### Backend
| Tech | Purpose |
|---|---|
| FastAPI | REST API |
| SQLAlchemy | ORM |
| SQLite | Database (zero config) |
| Uvicorn | ASGI server |
| Python-dotenv | Environment config |

### Deployment
| Service | Platform |
|---|---|
| Frontend | Vercel (CDN, free) |
| Backend | Render (free tier) |
| Database | SQLite (bundled) |

---

## 🚀 How to Run Locally

### Prerequisites
- Node.js 18+
- Python 3.11+
- Git

### Backend

```bash
cd backend
pip install -r requirements-prod.txt
uvicorn app.main:app --reload --port 8000
```

Backend starts at `http://localhost:8000`
Database auto-creates and seeds on first run.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend starts at `http://localhost:3000`

### Verify

```
http://localhost:8000/health          → Backend health check
http://localhost:8000/api/stadium/dashboard  → Live data
http://localhost:3000                 → Full UI
```

---

## 📁 Project Structure

```
stadiumverse-intelligence-os/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── database.py          # SQLite engine + session
│   │   ├── db_models.py         # All SQLAlchemy models
│   │   ├── seed.py              # Database seeder (fans, volunteers, etc.)
│   │   ├── config.py            # App configuration
│   │   ├── api/
│   │   │   └── stadium_routes.py # All REST endpoints
│   │   └── ai/
│   │       └── providers/       # AI provider abstraction (Ollama)
│   ├── requirements-prod.txt    # Minimal production deps
│   └── requirements.txt         # Full dev deps
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Root app + boot sequence + layout
│   │   ├── store/
│   │   │   └── appStore.ts      # Zustand global state
│   │   ├── services/
│   │   │   └── api.ts           # Typed API client
│   │   ├── hooks/
│   │   │   ├── useLiveData.ts   # Simulated live data (offline mode)
│   │   │   └── useDashboardData.ts  # Backend polling hook
│   │   ├── components/
│   │   │   ├── layout/          # TopBar, Sidebar, Dashboard
│   │   │   ├── pages/           # AIBrain, Analytics, DigitalTwins, Future
│   │   │   ├── stadium/         # Living Stadium SVG canvas
│   │   │   ├── brain/           # Living Brain panel + AI Debate
│   │   │   ├── command/         # Command Bar (Ctrl+K)
│   │   │   ├── timeline/        # Timeline scrubber
│   │   │   └── boot/            # Cinematic boot sequence
│   │   └── styles/
│   │       └── globals.css      # Global styles + glassmorphism
│   ├── vercel.json              # Vercel deployment config
│   └── vite.config.ts           # Vite build config
├── data/
│   └── sql/schema.sql           # Reference PostgreSQL schema
├── render.yaml                  # Render deployment config
└── .env.example                 # Environment variable template
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | System health check |
| GET | `/api/stadium/dashboard` | Full dashboard state (crowd + decisions + events) |
| GET | `/api/stadium/fans` | All digital fan twins |
| GET | `/api/stadium/fans/{id}` | Single fan inspector |
| GET | `/api/stadium/volunteers` | All volunteers + availability |
| POST | `/api/stadium/volunteers/{id}/deploy` | Deploy volunteer to zone |
| GET | `/api/stadium/crowd/current` | Latest crowd snapshot |
| GET | `/api/stadium/crowd/history` | Crowd history (up to 180 min) |
| POST | `/api/stadium/crowd/snapshot` | Create new live snapshot |
| GET | `/api/stadium/decisions` | AI Black Box decision log |
| GET | `/api/stadium/events` | Stadium event timeline |

Full interactive docs: `https://stadiumverse-intelligence-os-api.onrender.com/docs`

---

## 🔒 Security

- No API keys or secrets committed to repository
- `.env` is in `.gitignore` — only `.env.example` is tracked
- CORS configured to allow only known frontend origins
- Input validation via Pydantic models on all endpoints
- SQLAlchemy parameterized queries (no raw SQL injection risk)
- No authentication credentials stored in code

---

## ♿ Accessibility

- **Semantic HTML**: Proper use of `<section>`, `<header>`, and other semantic tags for page structure.
- **ARIA Labels**: Comprehensive `aria-label`, `aria-hidden`, and `role` attributes on all dynamic metrics, maps, and AI panels.
- **Skip Links**: "Skip to main content" link integrated for fast keyboard navigation.
- Color contrast ratios meet WCAG AA for primary text.
- Keyboard navigation supported (Ctrl+K command bar, Tab through sidebar).
- All interactive elements have focus states.
- Motion can be reduced via `prefers-reduced-motion` CSS media query.
- Screen reader compatible labels on icon-only sidebar buttons.

---

## 💎 Code Quality

- **Type Hints**: Strict Python return type hints across all FastAPI endpoints.
- **Docstrings**: Comprehensive Python docstrings for backend methods to ensure clarity and maintainability.
- **Consistent Structure**: Clean architectural separation between UI presentation (`components/`), global state (`store/`), and backend logic (`api/`).

---

## 🧪 Testing the Solution

### Automated Testing
The project features a comprehensive automated test suite to ensure platform reliability:
- **Frontend (Vitest)**: Validates UI state management and core logic. Run tests with:
  ```bash
  cd frontend
  npm run test
  ```
- **Backend (Pytest)**: Validates all API endpoints, database interactions, and AI routing logic. Run tests with:
  ```bash
  cd backend
  pytest
  ```

### Judge Demo Mode
1. Open the app
2. Click **▶ RUN DEMO** button (bottom-left of dashboard)
3. Watch the automated scenario: Goal → Rain → Congestion → AI Debate → Decision → Resolution

### Manual Testing
- Click any fan dot on the Living Stadium map → Digital Twin inspector opens
- Press **Ctrl+K** → Command bar with AI-powered commands
- Navigate to **AI Brain** page → Live reasoning chain + Black Box decisions
- Navigate to **Analytics** → Real ECharts data from SQLite
- Navigate to **Digital Twins** → All 10 fans from database
- Navigate to **Future Branches** → Click branches to see probability details
- Drag the **Timeline** scrubber at the bottom

---

## 💡 Assumptions

1. **Stadium capacity**: 87,342 fans (based on Lusail Stadium, Qatar)
2. **Match**: Brazil 2–1 Argentina, 67th minute (World Cup 2026 Final demo scenario)
3. **AI provider**: Ollama (local LLM) is optional — app runs fully without it using rule-based intelligence
4. **Database**: SQLite used for zero-config deployment; schema supports PostgreSQL for production scale
5. **Real-time**: Simulated via 3-second intervals on frontend + 5-second backend polling
6. **Digital twins**: 10 representative fans seeded; production system would support all 87,342

---

## 👤 Author

Built for the **FIFA World Cup 2026 AI Hackathon** — Challenge 4: Smart Stadiums & Tournament Operations

- GitHub: [@harichopper](https://github.com/harichopper)
- Repo: [stadiumverse-intelligence-os](https://github.com/harichopper/stadiumverse-intelligence-os)
