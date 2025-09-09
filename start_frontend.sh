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

# Check if Python is installed (for simple HTTP server)
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Start the frontend server
echo "Starting frontend server on http://localhost:3000"
echo "Make sure the backend is running on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m http.server 3000