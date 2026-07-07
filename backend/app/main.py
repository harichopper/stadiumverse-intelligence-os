"""
StadiumVerse Intelligence OS — Backend
FastAPI + SQLite | Production-ready
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

from .database import init_db
from .seed import run_seed

# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧠 StadiumVerse Intelligence OS — starting up")
    try:
        init_db()
        run_seed()
        logger.info("✅ DB ready")
    except Exception as e:
        logger.error(f"DB init error: {e}")
    yield
    logger.info("StadiumVerse Intelligence OS — shutdown")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="StadiumVerse Intelligence OS",
    description="AI Operating System for FIFA World Cup stadium management",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow Vercel + localhost
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
ALLOWED_ORIGINS += [
    "http://localhost:3000", "http://localhost:3001",
    "http://127.0.0.1:3000", "http://127.0.0.1:3001",
    "http://localhost:5173",
]
# Also allow all Vercel preview URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # we'll tighten after deploy
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
from .api.stadium_routes import router as stadium_router
app.include_router(stadium_router)

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "StadiumVerse Intelligence OS",
        "version": "2.0.0",
        "db": "sqlite",
    }

@app.get("/")
async def root():
    return {
        "name": "StadiumVerse Intelligence OS",
        "description": "AI Operating System for FIFA World Cup 2026",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/stadium/dashboard",
    }
