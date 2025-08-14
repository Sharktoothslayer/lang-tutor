from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import uuid


class UserVocabularyProgress(Base):
    __tablename__ = "user_vocabulary_progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    vocabulary_id = Column(String, ForeignKey("vocabulary.id"), nullable=False)
    
    # SM-2 algorithm fields
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=0)
    repetitions = Column(Integer, default=0)
    mastery_level = Column(Integer, default=0)  # 0-5 scale
    
    # Review tracking
    next_review = Column(DateTime, default=func.now())
    last_reviewed = Column(DateTime, default=func.now())
    
    # Performance tracking
    total_reviews = Column(Integer, default=0)
    correct_reviews = Column(Integer, default=0)
    response_time_avg = Column(Float, default=0.0)
    
    # Status
    is_learning = Column(Boolean, default=True)
    is_mastered = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="vocabulary_progress")
    vocabulary = relationship("Vocabulary", back_populates="user_progress")
    
    def __repr__(self):
        return f"<UserVocabularyProgress(user_id={self.user_id}, vocabulary_id={self.vocabulary_id})>"
