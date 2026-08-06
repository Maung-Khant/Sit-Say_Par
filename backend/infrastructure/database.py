# backend/infrastructure/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.infrastructure.models import Base

DATABASE_URL = "sqlite:///analysis.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Provide a database session and close it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
