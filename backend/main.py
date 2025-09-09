from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional

# Create FastAPI instance
app = FastAPI(
    title="Hello World API",
    description="A simple FastAPI backend for Hello World demo",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Hello World API!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "hello": "/hello",
            "personalized": "/hello/{name}",
            "api_message": "/api/message"
        }
    }

@app.get("/hello")
async def hello_world():
    """Basic hello world endpoint"""
    return {
        "message": "Hello, World!",
        "timestamp": datetime.now().isoformat(),
        "source": "FastAPI Backend"
    }

@app.get("/hello/{name}")
async def hello_name(name: str):
    """Personalized greeting endpoint"""
    return {
        "message": f"Hello, {name}!",
        "name": name,
        "timestamp": datetime.now().isoformat(),
        "source": "FastAPI Backend"
    }

@app.get("/api/message")
async def get_message(name: Optional[str] = None):
    """API endpoint for frontend consumption"""
    if name:
        message = f"Hello, {name}! Welcome to our Vue 3 + FastAPI demo!"
    else:
        message = "Hello, World! This message comes from FastAPI backend."
    
    return {
        "success": True,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "backend": "FastAPI",
        "frontend": "Vue 3.js"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Hello World API"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)