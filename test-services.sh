#!/bin/bash

echo "🧪 Testing Lang-Tutor Services"
echo "==============================="

# Test PostgreSQL
echo "📊 Testing PostgreSQL..."
if docker exec lang-tutor-postgres pg_isready -U langtutor > /dev/null 2>&1; then
    echo "✅ PostgreSQL: Running and accessible"
else
    echo "❌ PostgreSQL: Not accessible"
fi

# Test Redis
echo "🔴 Testing Redis..."
if docker exec lang-tutor-redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis: Running and accessible"
else
    echo "❌ Redis: Not accessible"
fi

# Test Backend API
echo "🔧 Testing Backend API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend API: Running and accessible"
    echo "   Health check response:"
    curl -s http://localhost:8000/health | jq . 2>/dev/null || curl -s http://localhost:8000/health
else
    echo "❌ Backend API: Not accessible"
fi

# Test Frontend
echo "🌐 Testing Frontend..."
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend: Running and accessible"
else
    echo "❌ Frontend: Not accessible"
fi

# Test Ollama
echo "🤖 Testing Ollama..."
if curl -s http://localhost:11435/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama: Running and accessible"
    echo "   Available models:"
    curl -s http://localhost:11435/api/tags | jq '.models[].name' 2>/dev/null || echo "   (JSON parsing not available)"
else
    echo "❌ Ollama: Not accessible"
fi

echo ""
echo "🎯 Next Steps:"
echo "1. If all services are ✅, you can start building the full React app"
echo "2. If some services are ❌, we need to fix those first"
echo "3. Access the basic frontend at: http://localhost:3000"
echo "4. Check API docs at: http://localhost:8000/docs"
