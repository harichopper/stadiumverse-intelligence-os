"""
StadiumVerse AI V2 - Database Configuration
SQLite database setup for development
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create SQLite engine
engine = create_engine(
    "sqlite:///./stadiumverse.db",
    connect_args={"check_same_thread": False}  # SQLite specific
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)