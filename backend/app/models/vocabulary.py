from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class Vocabulary(Base):
    __tablename__ = "vocabulary"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    word = Column(String(100), nullable=False)
    translation = Column(String(200), nullable=False)
    part_of_speech = Column(String(50), nullable=False)
    example_sentence = Column(Text, nullable=False)
    pronunciation = Column(String(100), nullable=False)
    
    # Language and difficulty
    language_code = Column(String(10), default="it")  # Default to Italian
    difficulty_level = Column(Integer, default=1)  # 1=easy, 5=hard
    frequency_rank = Column(Integer, default=1000)  # Lower = more common
    
    # Additional metadata
    tags = Column(String(200))  # Comma-separated tags
    notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user_progress = relationship("UserVocabularyProgress", back_populates="vocabulary")
    
    def __repr__(self):
        return f"<Vocabulary(word='{self.word}', translation='{self.translation}')>"
