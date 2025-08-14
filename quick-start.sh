#!/bin/bash

# Lang-Tutor Quick Start Script for Unraid
# This script will help you get the system running quickly

set -e

echo "🚀 Lang-Tutor Quick Start Script"
echo "=================================="

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
    
    # Generate a random secret key
    SECRET_KEY=$(openssl rand -hex 32)
    sed -i "s/your-secret-key-here-change-this-in-production/$SECRET_KEY/" .env
    
    # Generate a random database password
    DB_PASSWORD=$(openssl rand -base64 16)
    sed -i "s/langtutor123/$DB_PASSWORD/" .env
    
    echo "✅ Created .env file with secure credentials"
    echo "📋 Database password: $DB_PASSWORD"
    echo "📋 Secret key: $SECRET_KEY"
    echo "⚠️  Please save these credentials securely!"
else
    echo "✅ .env file already exists"
fi

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
docker exec -it lang-tutor-ollama ollama pull mistral:7b || {
    echo "⚠️  Failed to download model. You can try manually later."
}

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
echo "   Frontend: http://$(hostname -I | awk '{print $1}'):3000"
echo "   Backend API: http://$(hostname -I | awk '{print $1}'):8000"
echo "   API Docs: http://$(hostname -I | awk '{print $1}'):8000/docs"
echo ""
echo "📚 Next steps:"
echo "   1. Open the frontend in your browser"
echo "   2. Register a new account"
echo "   3. Start learning!"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart services: docker-compose restart"
echo "   Check status: docker-compose ps"
echo ""
echo "📖 For detailed setup instructions, see setup.md"
echo "🐛 For troubleshooting, check the logs or see setup.md" 