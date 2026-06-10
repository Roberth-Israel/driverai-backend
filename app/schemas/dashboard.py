import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RideSummary(BaseModel):
    id: uuid.UUID
    origin: str
    destination: str
    distance: float
    fare: float
    driver_earnings: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    daily_earnings: float
    weekly_earnings: float
    monthly_earnings: float
    net_profit: float
    fuel_cost: float
    energy_cost: float
    avg_per_hour: float
    avg_per_km: float
    total_rides: int
    accepted_rides: int
    rejected_rides: int
    avg_rating: float
    recent_rides: List[RideSummary]
