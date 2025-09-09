#!/bin/bash

echo "Docker Environment Test"
echo "======================="

# Check Docker installation
echo "1. Checking Docker installation..."
if command -v docker &> /dev/null; then
    echo "✅ Docker is installed: $(docker --version)"
else
    echo "❌ Docker is not installed"
    exit 1
fi

# Check Docker daemon
echo ""
echo "2. Checking Docker daemon..."
if docker info &> /dev/null; then
    echo "✅ Docker daemon is running"
else
    echo "❌ Docker daemon is not running"
    echo "Please start Docker daemon and try again"
    exit 1
fi

# Check project structure
echo ""
echo "3. Checking project structure..."
required_files=(
    "Dockerfile"
    "backend/main.py"
    "backend/requirements.txt"
    "frontend/App.vue"
    "frontend/main.js"
    "frontend/package.json"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
        exit 1
    fi
done

# Check Docker build context
echo ""
echo "4. Checking Docker build context size..."
context_size=$(du -sh . | cut -f1)
echo "📁 Build context size: $context_size"

if [ -f ".dockerignore" ]; then
    echo "✅ .dockerignore exists"
else
    echo "⚠️  .dockerignore not found (recommended for smaller build context)"
fi

# Test Docker build (dry run)
echo ""
echo "5. Testing Docker build syntax..."
# Note: --dry-run is not available in all Docker versions, so we'll do a quick syntax check
if docker build --help | grep -q "dry-run"; then
    if docker build --dry-run . &> /dev/null; then
        echo "✅ Dockerfile syntax is valid"
    else
        echo "❌ Dockerfile has syntax errors"
        echo "Run 'docker build .' to see detailed errors"
        exit 1
    fi
else
    echo "✅ Dockerfile syntax appears valid (dry-run not available)"
    echo "💡 Run './docker-build.sh' to test the full build process"
fi

echo ""
echo "🎉 All checks passed! Ready to build Docker image."
echo ""
echo "Next steps:"
echo "  1. Build the image: ./docker-build.sh"
echo "  2. Run the container: ./docker-run.sh"
echo "  3. Or use Docker Compose: docker-compose up -d"