#!/bin/bash

echo "🚀 Lang-Tutor Single Container Setup"
echo "====================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Create data directory
echo "📁 Creating data directory..."
mkdir -p /mnt/user/appdata/lang-tutor/data

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.txt .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env file and set secure passwords before continuing"
    echo ""
    read -p "Press Enter to continue..."
else
    echo "✅ .env file already exists"
fi

# Build and start the single container
echo "🔨 Building single container..."
docker-compose -f docker-compose-single.yml build

echo "🚀 Starting Lang-Tutor single container..."
docker-compose -f docker-compose-single.yml up -d

echo "⏳ Waiting for services to start..."
sleep 20

# Check container status
echo "📊 Container Status:"
docker-compose -f docker-compose-single.yml ps

echo ""
echo "🎉 Setup complete! Your Lang-Tutor system is now running in a single container."
echo ""
echo "🌐 Access your application at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "🇮🇹 Italian Language Learning Setup:"
echo "   - Target language set to Italian"
echo "   - AI tutor will converse in Italian"
echo "   - All services running in one container"
echo ""
echo "🔧 Useful commands:"
echo "   View logs: docker-compose -f docker-compose-single.yml logs -f"
echo "   Stop services: docker-compose -f docker-compose-single.yml down"
echo "   Restart services: docker-compose -f docker-compose-single.yml restart"
echo "   Check status: docker-compose -f docker-compose-single.yml ps"
