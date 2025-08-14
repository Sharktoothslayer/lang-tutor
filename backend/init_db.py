#!/usr/bin/env python3
"""
Database initialization script for LangTutor
"""
import asyncio
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.core.database import Base, engine
from app.models.user import User

def init_database():
    """Initialize the database with tables and basic data"""
    print("🚀 Initializing LangTutor database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    # Test database connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Database connection successful: {version}")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    print("🎉 Database initialization completed successfully!")
    return True

if __name__ == "__main__":
    init_database()
