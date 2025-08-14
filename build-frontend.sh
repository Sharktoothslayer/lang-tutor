#!/bin/bash

echo "🔨 Building Lang-Tutor React Frontend"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the lang-tutor root directory"
    exit 1
fi

# Go to frontend directory
cd frontend

echo "📦 Installing dependencies..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "🔨 Building React app..."
npm run build

if [ $? -ne 0 ]; then
    echo "❌ Failed to build React app"
    exit 1
fi

echo "✅ Frontend built successfully!"
echo ""
echo "🚀 Now rebuild your containers:"
echo "   docker-compose down"
echo "   docker-compose up -d --build"
echo ""
echo "🌐 Your new React app will be available at: http://localhost:3000"
