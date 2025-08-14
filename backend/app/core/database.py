from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Import models to register them with SQLAlchemy
from app.models.user import User
from app.models.vocabulary import Vocabulary
from app.models.user_vocabulary_progress import UserVocabularyProgress

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async dependency to get database session
async def get_async_db():
    # For now, return the sync session wrapped in an async context
    # In production, you'd want to use a proper async database
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
