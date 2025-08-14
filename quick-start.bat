@echo off
chcp 65001 >nul
echo 🚀 Lang-Tutor Quick Start Script for Unraid
echo ==============================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker first.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install it first.
    pause
    exit /b 1
)

echo ✅ docker-compose is available

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy env.example .env
    
    echo ✅ Created .env file
    echo ⚠️  Please edit .env file and set secure passwords before continuing
    echo.
    pause
) else (
    echo ✅ .env file already exists
)

REM Pull the latest images
echo 📥 Pulling Docker images...
docker-compose pull

REM Start Ollama service first to download the model
echo 🤖 Starting Ollama service...
docker-compose up -d ollama

echo ⏳ Waiting for Ollama to start...
timeout /t 10 /nobreak >nul

REM Download the AI model
echo 📚 Downloading AI model (this may take a while)...
docker exec -it lang-tutor-ollama ollama pull mistral:7b
if %errorlevel% neq 0 (
    echo ⚠️  Failed to download model. You can try manually later.
)

REM Start all services
echo 🚀 Starting all services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 15 /nobreak >nul

REM Check service status
echo 📊 Service Status:
docker-compose ps

echo.
       echo 🎉 Setup complete! Your Lang-Tutor system is now running.
       echo.
       echo 🌐 Access your application at:
       echo    Frontend: http://localhost:3000
       echo    Backend API: http://localhost:8000
       echo    API Docs: http://localhost:8000/docs
       echo.
       echo 🇮🇹 Italian Language Learning Setup:
       echo    - Target language set to Italian
       echo    - AI tutor will converse in Italian
       echo    - Vocabulary focused on Italian words
       echo.
       echo 📚 Next steps:
       echo    1. Open the frontend in your browser
       echo    2. Register a new account
       echo    3. Start learning Italian!
echo.
echo 🔧 Useful commands:
echo    View logs: docker-compose logs -f
echo    Stop services: docker-compose down
echo    Restart services: docker-compose restart
echo    Check status: docker-compose ps
echo.
echo 📖 For detailed setup instructions, see setup.md
echo 🐛 For troubleshooting, check the logs or see setup.md
echo.
pause 