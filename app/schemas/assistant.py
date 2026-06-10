from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    confidence: float = 1.0
    suggested_regions: Optional[list] = None
