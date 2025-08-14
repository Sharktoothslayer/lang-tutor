from sqlalchemy import Column, String, DateTime, Boolean, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from passlib.hash import bcrypt
from app.core.database import Base
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=False)  # Changed to match DB schema
    password_hash = Column(String(255), nullable=False)
    native_language = Column(String(10), default="en")
    target_language = Column(String(10), default="it")  # Changed to Italian
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={})
    
    @property
    def id_str(self):
        """Convert UUID to string for API serialization"""
        return str(self.id)
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)
    
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hash(password) 