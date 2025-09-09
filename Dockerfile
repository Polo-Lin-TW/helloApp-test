# Multi-stage build for Hello World Web App
# Stage 1: Build Vue 3 frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./
COPY frontend/vite.config.js ./

# Install frontend dependencies (including devDependencies for build)
RUN npm ci

# Copy frontend source code
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 2: Setup Python backend and serve the app
FROM python:3.11-slim AS production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FRONTEND_DIR=/app/frontend/dist
ENV BACKEND_DIR=/app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source code
COPY backend/ ./backend/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy static frontend files (fallback for non-Vite setup)
COPY frontend/index.html ./frontend/
COPY frontend/App.vue ./frontend/
COPY frontend/main.js ./frontend/

# Create a startup script
RUN cat > /app/start.sh << 'EOF'
#!/bin/bash

echo "Starting Hello World Web App..."
echo "================================"

# Start FastAPI backend in background
echo "Starting FastAPI backend on port 8000..."
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Check if backend is running
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is running successfully"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Serve frontend using Python HTTP server
echo "Starting frontend server on port 3000..."
cd /app/frontend
if [ -d "dist" ]; then
    echo "Serving built frontend from dist/"
    cd dist
    python3 -m http.server 3000 &
else
    echo "Serving development frontend"
    python3 -m http.server 3000 &
fi
FRONTEND_PID=$!

echo ""
echo "🚀 Application is ready!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the application"

# Function to handle shutdown
cleanup() {
    echo ""
    echo "Shutting down application..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Wait for processes
wait
EOF

# Make startup script executable
RUN chmod +x /app/start.sh

# Expose ports
EXPOSE 3000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health && curl -f http://localhost:3000/ || exit 1

# Set the startup script as entrypoint
ENTRYPOINT ["/app/start.sh"]

# Metadata
LABEL maintainer="Developer"
LABEL description="Hello World Web App with Vue 3.js frontend and FastAPI backend"
LABEL version="1.0.0"