from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional, List
from database import db
from models import MessageCreate, MessageResponse, ApiResponse

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

# Database startup and shutdown events
@app.on_event("startup")
async def startup():
    await db.init_pool()

@app.on_event("shutdown")
async def shutdown():
    await db.close_pool()

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Welcome to Hello World API!",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "hello": "/hello",
            "personalized": "/hello/{name}",
            "api_message": "/api/message",
            "messages": "/api/messages",
            "add_message": "/api/messages (POST)"
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

# Database endpoints
@app.post("/api/messages", response_model=ApiResponse)
async def create_message(message_data: MessageCreate):
    """Create a new message and store it in the database"""
    try:
        message_id = await db.insert_message(message_data.name, message_data.message)
        return ApiResponse(
            success=True,
            message="Message created successfully",
            data={"id": message_id, "name": message_data.name, "message": message_data.message}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/messages", response_model=ApiResponse)
async def get_messages(limit: int = 100):
    """Get all messages from the database"""
    try:
        messages = await db.get_messages(limit)
        return ApiResponse(
            success=True,
            message=f"Retrieved {len(messages)} messages",
            data={"messages": messages, "count": len(messages)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/messages/{message_id}", response_model=ApiResponse)
async def get_message_by_id(message_id: int):
    """Get a specific message by ID"""
    try:
        message = await db.get_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return ApiResponse(
            success=True,
            message="Message retrieved successfully",
            data={"message": message}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)