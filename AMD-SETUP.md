# AMD System Optimization for Lang-Tutor

This guide provides specific optimizations for running Lang-Tutor on AMD systems like your Ryzen 5 7640HS with Radeon 760M Graphics.

## System Specifications
- **CPU**: AMD Ryzen 5 7640HS @ 4.3 GHz
- **GPU**: AMD Radeon 760M Graphics
- **Architecture**: Zen 4 (RDNA 3 graphics)

## AMD-Specific Optimizations

### 1. ROCm Support (Optional)
If you want to use AMD GPU acceleration with ROCm:

```bash
# Install ROCm (Ubuntu/Debian)
wget -q -O - https://repo.radeon.com/rocm/rocm.gpg.key | sudo apt-key add -
echo 'deb [arch=amd64] https://repo.radeon.com/rocm/apt/debian ubuntu main' | sudo tee /etc/apt/sources.list.d/rocm.list
sudo apt update
sudo apt install rocm-hip-sdk

# Enable ROCm in Docker Compose
# Uncomment the runtime: rocm line in docker-compose.yml
```

### 2. CPU Optimization
Your 6-core Ryzen 5 7640HS is well-suited for language models:

```yaml
# In docker-compose.yml, add CPU limits
ollama:
  deploy:
    resources:
      limits:
        cpus: '4.0'  # Use 4 cores, leave 2 for system
        memory: 8G
      reservations:
        cpus: '2.0'  # Reserve 2 cores
        memory: 4G
```

### 3. Model Selection for AMD
For your system, these models work well:

- **mistral:7b** (default) - Good balance of speed/quality
- **llama2:7b** - Alternative option
- **codellama:7b** - If you want coding assistance too

### 4. Performance Tuning

#### Environment Variables
```bash
# Add to .env file
OLLAMA_NUM_PARALLEL=4
OLLAMA_GPU_LAYERS=32
OLLAMA_CPU_THREADS=6
```

#### Docker Compose Optimizations
```yaml
ollama:
  environment:
    - OLLAMA_HOST=0.0.0.0
    - OLLAMA_MODEL=mistral:7b
    - OLLAMA_NUM_PARALLEL=4
    - OLLAMA_GPU_LAYERS=32
    - OLLAMA_CPU_THREADS=6
  deploy:
    resources:
      limits:
        cpus: '4.0'
        memory: 8G
      reservations:
        cpus: '2.0'
        memory: 4G
```

### 5. Memory Management
Your system has good memory bandwidth. Optimize for it:

```yaml
# PostgreSQL optimization
postgres:
  environment:
    - POSTGRES_SHARED_BUFFERS=1GB
    - POSTGRES_EFFECTIVE_CACHE_SIZE=3GB
    - POSTGRES_WORK_MEM=16MB
    - POSTGRES_MAINTENANCE_WORK_MEM=256MB
```

### 6. Network Optimization
For better performance between containers:

```yaml
# In docker-compose.yml
networks:
  default:
    name: lang-tutor-network
    driver: bridge
    driver_opts:
      com.docker.network.bridge.enable_icc: "true"
      com.docker.network.bridge.enable_ip_masquerade: "true"
```

## Performance Expectations

### With CPU Only (Default)
- **Response Time**: 2-5 seconds for typical responses
- **Memory Usage**: 6-8GB RAM
- **CPU Usage**: 60-80% during generation

### With ROCm GPU Acceleration
- **Response Time**: 1-3 seconds for typical responses
- **Memory Usage**: 6-8GB RAM + 2-4GB VRAM
- **GPU Usage**: 70-90% during generation

## Monitoring Performance

### Check Ollama Performance
```bash
# Monitor Ollama container
docker stats lang-tutor-ollama

# Check Ollama logs
docker logs -f lang-tutor-ollama

# Test model performance
docker exec -it lang-tutor-ollama ollama list
```

### System Resource Monitoring
```bash
# CPU and memory usage
htop

# GPU usage (if using ROCm)
rocm-smi

# Disk I/O
iotop
```

## Troubleshooting AMD Issues

### Common Issues and Solutions

#### 1. High CPU Usage
```bash
# Reduce parallel processing
export OLLAMA_NUM_PARALLEL=2

# Limit CPU threads
export OLLAMA_CPU_THREADS=4
```

#### 2. Memory Issues
```bash
# Check available memory
free -h

# Reduce model context
export OLLAMA_MAX_TOKENS=1024
```

#### 3. ROCm Issues
```bash
# Check ROCm installation
rocm-smi

# Verify GPU detection
docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
# (This will show AMD GPU info if ROCm is working)
```

## Recommended Settings for Your System

Based on your Ryzen 5 7640HS specifications:

```yaml
# Optimal docker-compose.yml settings
ollama:
  environment:
    - OLLAMA_HOST=0.0.0.0
    - OLLAMA_MODEL=mistral:7b
    - OLLAMA_NUM_PARALLEL=3
    - OLLAMA_CPU_THREADS=4
    - OLLAMA_MAX_TOKENS=2048
  deploy:
    resources:
      limits:
        cpus: '3.5'
        memory: 6G
      reservations:
        cpus: '2.0'
        memory: 3G
```

## Next Steps

1. **Start with CPU-only mode** to establish baseline performance
2. **Monitor system resources** during typical usage
3. **Gradually increase parallel processing** if performance allows
4. **Consider ROCm** if you need faster response times
5. **Adjust memory limits** based on your system's available RAM

Your system should handle the language learning workload very well, providing responsive AI conversations while maintaining good system performance for other tasks.
