#!/bin/bash

echo "Starting FastAPI Backend..."
echo "================================"

# Check if we're in the right directory
if [ ! -d "backend" ]; then
    echo "Error: backend directory not found. Please run this script from the project root."
    exit 1
fi

# Navigate to backend directory
cd backend

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Check if pip is installed (try pip3 first, then pip)
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "Error: pip is not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Start the FastAPI server
echo "Starting FastAPI server on http://localhost:8000"
echo "API documentation will be available at http://localhost:8000/docs"
echo "Press Ctrl+C to stop the server"
echo ""

# Use the virtual environment's uvicorn
if [ -f "../.venv/bin/uvicorn" ]; then
    ../.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
elif [ -f "../.venv/bin/python" ]; then
    ../.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi