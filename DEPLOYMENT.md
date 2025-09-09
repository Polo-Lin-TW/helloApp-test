# Deployment Guide

This document provides comprehensive instructions for deploying the Hello World Web App using Docker.

## 🐳 Docker Deployment Options

### Option 1: Single Container (Recommended)

Uses the root `Dockerfile` to build a single container with both frontend and backend.

#### Quick Start
```bash
# Build the Docker image
./docker-build.sh

# Run the application
./docker-run.sh
```

#### Manual Commands
```bash
# Build the image
docker build -t hello-world-webapp:latest .

# Run the container
docker run -d \
  --name hello-world-app \
  -p 3000:3000 \
  -p 8000:8000 \
  --restart unless-stopped \
  hello-world-webapp:latest
```

### Option 2: Docker Compose

Uses `docker-compose.yml` for orchestrated deployment.

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

## 📋 Dockerfile Architecture

### Multi-Stage Build Process

#### Stage 1: Frontend Builder
```dockerfile
FROM node:18-alpine AS frontend-builder
# - Installs Node.js dependencies
# - Builds Vue 3 frontend with Vite
# - Creates optimized production bundle
```

#### Stage 2: Production Runtime
```dockerfile
FROM python:3.11-slim AS production
# - Sets up Python environment
# - Installs FastAPI dependencies
# - Copies built frontend from Stage 1
# - Creates startup script for both services
```

### Key Features

1. **Multi-stage build** for optimized image size
2. **Health checks** for both frontend and backend
3. **Graceful shutdown** handling
4. **Production-ready** configuration
5. **Automatic service startup** with monitoring

## 🚀 Application Access

Once deployed, the application will be available at:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PYTHONDONTWRITEBYTECODE` | `1` | Prevents Python from writing .pyc files |
| `PYTHONUNBUFFERED` | `1` | Ensures Python output is sent straight to terminal |
| `FRONTEND_DIR` | `/app/frontend/dist` | Frontend build directory |
| `BACKEND_DIR` | `/app/backend` | Backend source directory |

### Port Configuration

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 3000 | Vue 3.js application |
| Backend | 8000 | FastAPI REST API |

## 📊 Monitoring and Health Checks

### Built-in Health Checks

The Docker container includes automatic health monitoring:

```bash
# Check container health status
docker ps

# View detailed health check logs
docker inspect hello-world-app | grep -A 10 Health
```

### Manual Health Verification

```bash
# Backend health
curl http://localhost:8000/health

# Frontend availability
curl -I http://localhost:3000/

# API functionality
curl http://localhost:8000/hello
```

## 🛠️ Development vs Production

### Development Mode
```bash
# Use local development servers
./start_backend.sh    # Terminal 1
./start_frontend.sh   # Terminal 2
```

### Production Mode
```bash
# Use Docker container
./docker-build.sh && ./docker-run.sh
```

## 📝 Container Management

### Useful Docker Commands

```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View container logs
docker logs -f hello-world-app

# Execute commands in container
docker exec -it hello-world-app bash

# Stop container
docker stop hello-world-app

# Remove container
docker rm hello-world-app

# Remove image
docker rmi hello-world-webapp:latest

# View image details
docker images hello-world-webapp
```

### Container Lifecycle

```bash
# Start stopped container
docker start hello-world-app

# Restart container
docker restart hello-world-app

# Pause container
docker pause hello-world-app

# Unpause container
docker unpause hello-world-app
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Find process using port
lsof -i :3000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### 2. Container Won't Start
```bash
# Check container logs
docker logs hello-world-app

# Check system resources
docker system df
docker system prune  # Clean up if needed
```

#### 3. Health Check Failures
```bash
# Check individual services
docker exec hello-world-app curl http://localhost:8000/health
docker exec hello-world-app curl http://localhost:3000/
```

#### 4. Build Failures
```bash
# Clean Docker cache
docker builder prune

# Rebuild without cache
docker build --no-cache -t hello-world-webapp:latest .
```

### Debug Mode

To run the container in debug mode:

```bash
# Run container interactively
docker run -it \
  -p 3000:3000 \
  -p 8000:8000 \
  hello-world-webapp:latest \
  bash

# Then manually start services for debugging
```

## 🚀 Production Deployment

### Cloud Deployment

#### Docker Hub
```bash
# Tag for Docker Hub
docker tag hello-world-webapp:latest username/hello-world-webapp:latest

# Push to Docker Hub
docker push username/hello-world-webapp:latest
```

#### AWS ECS/Fargate
```bash
# Tag for ECR
docker tag hello-world-webapp:latest 123456789012.dkr.ecr.region.amazonaws.com/hello-world-webapp:latest

# Push to ECR
docker push 123456789012.dkr.ecr.region.amazonaws.com/hello-world-webapp:latest
```

### Environment-Specific Configurations

#### Production Environment Variables
```bash
docker run -d \
  --name hello-world-app-prod \
  -p 80:3000 \
  -p 8080:8000 \
  -e NODE_ENV=production \
  -e PYTHONPATH=/app/backend \
  --restart always \
  hello-world-webapp:latest
```

## 📈 Performance Optimization

### Image Size Optimization
- Multi-stage builds reduce final image size
- `.dockerignore` excludes unnecessary files
- Alpine Linux base images for smaller footprint

### Runtime Optimization
- Health checks ensure service availability
- Restart policies handle failures automatically
- Resource limits can be set for production

### Monitoring
```bash
# Monitor resource usage
docker stats hello-world-app

# Monitor logs in real-time
docker logs -f hello-world-app
```

## 🔐 Security Considerations

1. **Non-root user**: Consider running services as non-root user
2. **Secrets management**: Use Docker secrets for sensitive data
3. **Network isolation**: Use custom Docker networks in production
4. **Image scanning**: Scan images for vulnerabilities
5. **Regular updates**: Keep base images and dependencies updated

## 📚 Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Vue.js Production Deployment](https://vuejs.org/guide/best-practices/production-deployment.html)
- [Container Security](https://docs.docker.com/engine/security/)