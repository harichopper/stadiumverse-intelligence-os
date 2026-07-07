"""
StadiumVerse Intelligence OS — Backend
FastAPI + SQLite | Production-ready
"""

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🧠 StadiumVerse Intelligence OS — starting up")
    # Only init/seed when NOT in test mode
    if os.getenv("TESTING") != "true":
        try:
            from .database import init_db
            from .seed import run_seed

            init_db()
            run_seed()
            logger.info("✅ DB ready")
        except Exception as exc:
            logger.error(f"DB init error: {exc}")
    yield
    logger.info("StadiumVerse Intelligence OS — shutdown")


app = FastAPI(
    title="StadiumVerse Intelligence OS - FIFA World Cup 2026",
    description="AI Operating System for Smart Stadiums & Tournament Operations",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
ALLOWED_ORIGINS += [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://localhost:5173",
]
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

from .api.stadium_routes import router as stadium_router  # noqa: E402

app.include_router(stadium_router)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "StadiumVerse Intelligence OS",
        "version": "2.0.0",
        "db": "sqlite",
    }


@app.get("/")
async def root():
    """Root endpoint — service info."""
    return {
        "name": "StadiumVerse Intelligence OS",
        "description": "AI Operating System for FIFA World Cup 2026",
        "docs": "/docs",
        "health": "/health",
        "api": "/api/stadium/dashboard",
    }
