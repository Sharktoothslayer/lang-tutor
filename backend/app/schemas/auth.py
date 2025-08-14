from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str  # Changed from EmailStr to str for simplicity
    native_language: str = "en"
    target_language: str = "it"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str  # Changed from EmailStr to str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    preferences: dict
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None
