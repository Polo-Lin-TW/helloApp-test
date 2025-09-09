#!/bin/bash

echo "Running Hello World Web App Docker Container"
echo "============================================"

# Set image name and container name
IMAGE_NAME="hello-world-webapp:latest"
CONTAINER_NAME="hello-world-app"

# Stop and remove existing container if it exists
echo "Cleaning up existing container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

# Run the Docker container
echo "Starting new container: $CONTAINER_NAME"
echo ""

docker run -d \
    --name $CONTAINER_NAME \
    -p 3000:3000 \
    -p 8000:8000 \
    --restart unless-stopped \
    $IMAGE_NAME

# Check if container started successfully
if [ $? -eq 0 ]; then
    echo "✅ Container started successfully!"
    echo ""
    echo "Container status:"
    docker ps | grep $CONTAINER_NAME
    echo ""
    echo "🚀 Application is now running:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Documentation: http://localhost:8000/docs"
    echo ""
    echo "To view logs:"
    echo "  docker logs -f $CONTAINER_NAME"
    echo ""
    echo "To stop the container:"
    echo "  docker stop $CONTAINER_NAME"
    echo ""
    echo "To remove the container:"
    echo "  docker rm $CONTAINER_NAME"
    
    # Wait a moment and check health
    echo "Checking application health in 10 seconds..."
    sleep 10
    
    echo ""
    echo "Health check results:"
    curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Backend health check failed"
    curl -s -o /dev/null -w "Frontend status: %{http_code}\n" http://localhost:3000/ 2>/dev/null || echo "Frontend health check failed"
    
else
    echo "❌ Failed to start container!"
    echo ""
    echo "Check the logs for more information:"
    echo "  docker logs $CONTAINER_NAME"
    exit 1
fi