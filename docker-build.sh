#!/bin/bash

echo "Building Hello World Web App Docker Image"
echo "=========================================="

# Set image name and tag
IMAGE_NAME="hello-world-webapp"
IMAGE_TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"

# Build the Docker image
echo "Building Docker image: $FULL_IMAGE_NAME"
echo ""

docker build -t $FULL_IMAGE_NAME .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Docker image built successfully!"
    echo ""
    echo "Image details:"
    docker images $IMAGE_NAME
    echo ""
    echo "To run the application:"
    echo "  docker run -p 3000:3000 -p 8000:8000 $FULL_IMAGE_NAME"
    echo ""
    echo "Or use the run script:"
    echo "  ./docker-run.sh"
    echo ""
    echo "To access the application:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
else
    echo ""
    echo "❌ Docker build failed!"
    exit 1
fi