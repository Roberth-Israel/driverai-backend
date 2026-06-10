import uuid
from pydantic import BaseModel
from typing import List
from datetime import datetime


class AlertResponse(BaseModel):
    id: uuid.UUID
    title: str
    message: str
    type: str
    severity: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    alerts: List[AlertResponse]
    unread_count: int
