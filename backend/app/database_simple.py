"""
StadiumVerse AI V2 - Simplified Database Configuration  
SQLite database setup for development without complex dependencies
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Create SQLite engine with a simple file database
DATABASE_PATH = "stadiumverse.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=False  # Set to True for SQL logging
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database dependency for FastAPI
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database tables
def init_db():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print(f"✅ SQLite database initialized: {DATABASE_PATH}")

# Check if database exists
def database_exists():
    """Check if database file exists"""
    return os.path.exists(DATABASE_PATH)

# Simple status check
def get_db_status():
    """Get database status information"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            return {
                "status": "connected",
                "database_path": DATABASE_PATH,
                "database_exists": database_exists(),
                "engine_pool_size": engine.pool.size()
            }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "database_path": DATABASE_PATH,
            "database_exists": database_exists()
        }