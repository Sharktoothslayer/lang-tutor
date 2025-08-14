# Unraid Setup Guide - Current Status

## ✅ Changes Made

1. **Removed obsolete `version` field** from docker-compose.yml
2. **Changed Ollama port** from 11434 to 11435 to avoid conflicts
3. **Removed NVIDIA GPU configuration** (not compatible with AMD)
4. **Added AMD-optimized settings** for your Ryzen 5 7640HS
5. **Configured persistent storage** for Unraid
6. **Created Linux-compatible quick-start script**

## 🚀 Next Steps

### 1. Make Script Executable
```bash
chmod +x quick-start.sh
```

### 2. Create .env File
```bash
cp env.example .env
nano .env
```

**Edit these values in .env:**
```bash
POSTGRES_PASSWORD=your-secure-password-here
SECRET_KEY=your-super-secret-key-here
```

### 3. Create Storage Directories
```bash
mkdir -p /mnt/user/appdata/lang-tutor/postgres
mkdir -p /mnt/user/appdata/lang-tutor/redis
mkdir -p /mnt/user/appdata/lang-tutor/ollama
```

### 4. Run Setup Script
```bash
./quick-start.sh
```

## 🔧 Manual Alternative

If you prefer manual setup:
```bash
# Pull images
docker-compose pull

# Start Ollama first
docker-compose up -d ollama

# Wait, then download model
docker exec -it lang-tutor-ollama ollama pull mistral:7b

# Start all services
docker-compose up -d
```

## 🌐 Access Points

- **Frontend**: http://your-unraid-ip:3000
- **Backend API**: http://your-unraid-ip:8000
- **API Docs**: http://your-unraid-ip:8000/docs
- **Ollama**: http://your-unraid-ip:11435

## 🐛 Troubleshooting

### Port Already in Use
- Ollama port changed to 11435
- If other ports conflict, change them in docker-compose.yml

### GPU Errors
- NVIDIA configuration removed
- Running on CPU only (good performance on your Ryzen 5)

### Permission Issues
```bash
# Fix directory permissions
chown -R 1000:1000 /mnt/user/appdata/lang-tutor/
```

## 📊 System Requirements

- **RAM**: 8GB+ (6GB allocated to Ollama)
- **CPU**: 4+ cores (3.5 allocated to Ollama)
- **Storage**: 10GB+ for models and data
- **Network**: Docker networking enabled

Your AMD Ryzen 5 7640HS should handle this workload very well!
