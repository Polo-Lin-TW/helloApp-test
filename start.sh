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