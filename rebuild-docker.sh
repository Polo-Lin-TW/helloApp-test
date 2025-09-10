#!/bin/bash

# Rebuild Docker script for Hello World App
# This script rebuilds the Docker image with proper cache handling

set -e  # Exit on any error

IMAGE_NAME="hello-world-app"
TAG="latest"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "🔄 Starting Docker rebuild process..."

# Stop and remove existing container if running
echo "🛑 Stopping existing containers..."
docker stop ${IMAGE_NAME} 2>/dev/null || true
docker rm ${IMAGE_NAME} 2>/dev/null || true

# Remove existing image to force complete rebuild
echo "🗑️  Removing existing image..."
docker rmi ${FULL_IMAGE_NAME} 2>/dev/null || true

# Build new image with no cache to ensure fresh build
echo "🏗️  Building Docker image (no cache)..."
docker build --no-cache -t ${FULL_IMAGE_NAME} .

# Optional: Remove dangling images to clean up
echo "🧹 Cleaning up dangling images..."
docker image prune -f

echo "✅ Docker rebuild completed successfully!"
echo "📋 Image: ${FULL_IMAGE_NAME}"

# Run the container
echo "🚀 Starting container..."
docker run -d --name ${IMAGE_NAME} -p 80:80 ${FULL_IMAGE_NAME}

echo "🎉 Container started successfully!"
echo "🌐 Access the app at: http://localhost"