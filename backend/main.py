from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.database import engine, Base, get_db
from app.routers import auth, vocabulary
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends
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
app.include_router(vocabulary.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to LangTutor API! 🇮🇹"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "LangTutor API is running"}

@app.get("/debug/db")
async def debug_database(db: Session = Depends(get_db)):
    """Debug endpoint to test database connectivity"""
    try:
        # Test basic database connection
        result = db.execute(text("SELECT 1 as test"))
        test_value = result.scalar()
        
        # Test if users table exists
        result = db.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'users'"))
        users_table_exists = result.scalar() > 0
        
        # Test users table structure
        users_info = {}
        if users_table_exists:
            result = db.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' ORDER BY ordinal_position"))
            columns = result.fetchall()
            users_info = {col[0]: col[1] for col in columns}
        
        # Check existing users
        existing_users = []
        if users_table_exists:
            result = db.execute(text("SELECT username, email, created_at FROM users LIMIT 5"))
            users = result.fetchall()
            existing_users = [{"username": u[0], "email": u[1], "created_at": str(u[2])} for u in users]
        
        return {
            "database_connection": "OK",
            "test_query": test_value,
            "users_table_exists": users_table_exists,
            "users_table_structure": users_info,
            "existing_users": existing_users
        }
    except Exception as e:
        return {
            "database_connection": "FAILED",
            "error": str(e),
            "error_type": type(e).__name__
        }

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