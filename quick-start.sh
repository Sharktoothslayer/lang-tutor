#!/bin/bash

echo "🚀 Lang-Tutor Quick Start Script for Unraid"
echo "============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

echo "✅ docker-compose is available"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env file and set secure passwords before continuing"
    echo ""
    read -p "Press Enter to continue..."
else
    echo "✅ .env file already exists"
fi

# Create persistent storage directories
echo "📁 Creating persistent storage directories..."
mkdir -p /mnt/user/appdata/lang-tutor/postgres
mkdir -p /mnt/user/appdata/lang-tutor/redis
mkdir -p /mnt/user/appdata/lang-tutor/ollama

# Pull the latest images
echo "📥 Pulling Docker images..."
docker-compose pull

# Start Ollama service first to download the model
echo "🤖 Starting Ollama service..."
docker-compose up -d ollama

echo "⏳ Waiting for Ollama to start..."
sleep 10

# Download the AI model
echo "📚 Downloading AI model (this may take a while)..."
docker exec -it lang-tutor-ollama ollama pull mistral:7b

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 15

# Check service status
echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 Setup complete! Your Lang-Tutor system is now running."
echo ""
echo "🌐 Access your application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🇮🇹 Italian Language Learning Setup:"
echo "   - Target language set to Italian"
echo "   - AI tutor will converse in Italian"
echo "   - Vocabulary focused on Italian words"
echo ""
echo "📚 Next steps:"
echo "   1. Open the frontend in your browser"
echo "   2. Register a new account"
echo "   3. Start learning Italian!"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Check status: docker-compose ps"
echo ""
echo "📖 For detailed setup instructions, see setup.md"
echo "🐛 For troubleshooting, check the logs or see setup.md" 