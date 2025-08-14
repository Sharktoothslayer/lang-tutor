from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.database import engine, Base
from app.routers import auth
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LangTutor API",
    description="AI-powered language learning platform with spaced repetition",
    version="1.0.0"
)

# Add CORS middleware with comprehensive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://192.168.0.223:3000",  # Frontend port
        "http://192.168.0.223:80",    # Nginx port
        "http://localhost:3000",       # Local development
        "http://localhost:80",         # Local nginx
        "http://192.168.0.223",       # IP without port
        "http://localhost",            # Local without port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight for 24 hours
)

# Include routers
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to LangTutor API! 🇮🇹"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "LangTutor API is running"}

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle OPTIONS requests for CORS preflight"""
    return {"message": "OK"}

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 