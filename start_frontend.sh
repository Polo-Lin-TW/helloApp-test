#!/bin/bash

echo "Starting Vue 3.js Frontend..."
echo "============================="

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "Error: frontend directory not found. Please run this script from the project root."
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if Node.js and npm are available for Vite development server
if command -v npm &> /dev/null && [ -f "package.json" ]; then
    echo "Using Vite development server (recommended)..."
    echo "Installing dependencies if needed..."
    npm install
    echo ""
    echo "Starting Vite dev server on http://localhost:3000"
    echo "Make sure the backend is running on http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    echo ""
    npm run dev
elif command -v python3 &> /dev/null; then
    echo "Using Python HTTP server (fallback)..."
    echo "Note: For better development experience, install Node.js and use 'npm run dev'"
    echo ""
    echo "Starting frontend server on http://localhost:3000"
    echo "Make sure the backend is running on http://localhost:8000"
    echo "Press Ctrl+C to stop the server"
    echo ""
    python3 -m http.server 3000
else
    echo "Error: Neither Node.js nor Python 3 is installed."
    echo "Please install Node.js (recommended) or Python 3 to run the frontend."
    exit 1
fi