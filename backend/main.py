from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Language Tutor API...")
    
    # Initialize services here
    logger.info("Language Tutor API started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Language Tutor API...")

# Create FastAPI app
app = FastAPI(
    title="Language Tutor API",
    description="AI-powered language learning platform with spaced repetition",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Language Tutor API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Language Tutor API",
        "docs": "/docs",
        "health": "/health"
    }

# Protected endpoint example
@app.get("/protected")
async def protected_route():
    return {
        "message": "This is a protected route",
        "note": "Authentication not yet implemented"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    ) 