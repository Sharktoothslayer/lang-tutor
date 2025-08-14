# Lang-Tutor Setup Guide for Unraid

This guide will walk you through setting up the complete AI-powered language learning system on your Unraid server.

## Prerequisites

- Unraid server with Docker support
- At least 8GB RAM (16GB recommended for AI models)
- 50GB+ free storage space
- GPU support (optional but recommended for AI performance)

## Step 1: Install Docker on Unraid

1. Go to your Unraid web interface
2. Navigate to **Apps** → **Docker**
3. Install Docker if not already installed
4. Ensure Docker service is running

## Step 2: Clone the Repository

```bash
# SSH into your Unraid server
ssh root@your-unraid-ip

# Navigate to your preferred directory
cd /mnt/user/appdata/

# Clone the repository
git clone https://github.com/yourusername/lang-tutor.git
cd lang-tutor
```

## Step 3: Configure Environment Variables

1. Copy the environment template:
```bash
cp env.example .env
```

2. Edit the `.env` file with your preferred settings:
```bash
nano .env
```

**Important settings to configure:**
- `POSTGRES_PASSWORD`: Set a strong password for PostgreSQL
- `SECRET_KEY`: Generate a random secret key for JWT tokens
- `OLLAMA_MODEL`: Choose your preferred AI model (default: mistral:7b)

## Step 4: Download AI Models

Before starting the system, download the AI model:

```bash
# Start just the Ollama service first
docker-compose up -d ollama

# Wait for it to start, then pull the model
docker exec -it lang-tutor-ollama ollama pull mistral:7b

# For better performance, you can also try:
# docker exec -it lang-tutor-ollama ollama pull llama2:7b
# docker exec -it lang-tutor-ollama ollama pull codellama:7b
```

## Step 5: Start the System

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs if needed
docker-compose logs -f
```

## Step 6: Initialize the Database

The database will be automatically initialized with the schema and sample data. You can verify by checking the logs:

```bash
docker-compose logs postgres
```

## Step 7: Access the Application

- **Frontend**: http://your-unraid-ip:3000
- **Backend API**: http://your-unraid-ip:8000
- **API Documentation**: http://your-unraid-ip:8000/docs
- **Ollama**: http://your-unraid-ip:11434

## Step 8: Create Your First User

1. Open the frontend in your browser
2. Click "Register" to create your account
3. Choose your native language and target language
4. Complete the registration

## Step 9: Add Vocabulary (Optional)

You can add custom vocabulary through the API or import from CSV:

```bash
# Example API call to add a word
curl -X POST "http://your-unraid-ip:8000/api/v1/vocabulary" \
  -H "Content-Type: application/json" \
  -d '{
    "word": "hola",
    "translation": "hello",
    "language_code": "es",
    "part_of_speech": "interjection",
    "example_sentence": "¡Hola! ¿Cómo estás?",
    "difficulty_level": 1
  }'
```

## Configuration Options

### AI Model Selection

Edit `.env` to change the AI model:

```bash
# For faster responses (smaller model)
OLLAMA_MODEL=tinyllama:1b

# For better quality (larger model)
OLLAMA_MODEL=llama2:13b

# For coding-focused learning
OLLAMA_MODEL=codellama:7b
```

### Performance Tuning

For better performance, adjust these settings in `.env`:

```bash
# Increase AI response quality
OLLAMA_TEMPERATURE=0.3

# Reduce response length for faster replies
OLLAMA_MAX_TOKENS=1024

# Adjust learning parameters
NEW_WORDS_PER_SESSION=3
REVIEW_WORDS_PER_SESSION=15
```

### GPU Acceleration

If you have an NVIDIA GPU:

1. Install NVIDIA Container Toolkit on Unraid
2. The Docker Compose file already includes GPU support
3. Verify GPU usage: `nvidia-smi`

## Monitoring and Maintenance

### Check System Health

```bash
# View all service statuses
docker-compose ps

# Check resource usage
docker stats

# View logs
docker-compose logs -f [service-name]
```

### Backup Database

```bash
# Create backup
docker exec lang-tutor-postgres pg_dump -U langtutor langtutor > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
docker exec -i lang-tutor-postgres psql -U langtutor langtutor < backup_file.sql
```

### Update the System

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Common Issues

1. **Ollama service won't start**
   - Check if you have enough RAM (at least 8GB)
   - Verify Docker has access to sufficient resources

2. **Database connection errors**
   - Ensure PostgreSQL container is running
   - Check if port 5432 is available
   - Verify database credentials in `.env`

3. **Frontend not loading**
   - Check if React build completed successfully
   - Verify nginx configuration
   - Check browser console for errors

4. **AI responses are slow**
   - Consider using a smaller model
   - Ensure adequate CPU/RAM resources
   - Check if GPU acceleration is working

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f backend
docker-compose logs -f ollama

# Check container resource usage
docker stats lang-tutor-ollama
docker stats lang-tutor-backend
```

## Security Considerations

1. **Change default passwords** in `.env`
2. **Use HTTPS** in production (configure nginx with SSL)
3. **Restrict network access** to necessary ports only
4. **Regular updates** for security patches
5. **Backup your data** regularly

## Performance Optimization

1. **Use SSD storage** for database and AI models
2. **Allocate sufficient RAM** (16GB+ recommended)
3. **Enable GPU acceleration** if available
4. **Monitor resource usage** and adjust accordingly
5. **Use appropriate AI model size** for your hardware

## Support and Community

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check the README for detailed API docs
- **Discord**: Join our community for help and discussions

## Next Steps

After successful setup:

1. **Customize vocabulary** for your target language
2. **Adjust learning parameters** in settings
3. **Set up daily learning goals**
4. **Explore AI conversation features**
5. **Monitor your learning progress**

Happy learning! 🚀 