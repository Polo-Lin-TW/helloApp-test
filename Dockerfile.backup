# Multi-stage Dockerfile for Hello World Web App
# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies (including dev dependencies for build)
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 2: Setup Backend and Final Image with Nginx
FROM python:3.9-alpine

# Set working directory
WORKDIR /app

# Install system dependencies using apk (Alpine package manager)
RUN apk add --no-cache \
    curl \
    nginx \
    bash

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Nginx configuration (Alpine uses different path)
COPY nginx.conf /etc/nginx/http.d/default.conf

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Set container metadata
LABEL app.name="hello-world-app" \
      app.version="1.0.0" \
      app.description="Hello World Vue3 + FastAPI Application with Nginx"

# Create a startup script that starts Nginx and backend
RUN echo '#!/bin/bash' > start.sh && \
    echo 'cd /app' >> start.sh && \
    echo 'echo "Starting Hello World Application with Nginx..."' >> start.sh && \
    echo '# Create nginx PID directory' >> start.sh && \
    echo 'mkdir -p /run/nginx' >> start.sh && \
    echo '# Start Nginx in background' >> start.sh && \
    echo 'nginx &' >> start.sh && \
    echo 'echo "Nginx started on port 80"' >> start.sh && \
    echo '# Start backend server' >> start.sh && \
    echo 'echo "Starting backend server on port 8000"' >> start.sh && \
    echo 'uvicorn backend.main:app --host 127.0.0.1 --port 8000' >> start.sh && \
    chmod +x start.sh

# Expose port 80 for Nginx (frontend + API proxy)
EXPOSE 80

# Health check via Nginx
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start the application
CMD ["./start.sh"]