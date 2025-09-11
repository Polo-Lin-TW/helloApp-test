from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MessageCreate(BaseModel):
    name: str
    message: str

class MessageResponse(BaseModel):
    id: int
    name: str
    message: str
    created_at: datetime
    updated_at: datetime

class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None