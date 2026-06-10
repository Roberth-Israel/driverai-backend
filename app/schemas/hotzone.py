import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class HotZoneResponse(BaseModel):
    id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    demand_intensity: float
    average_earnings_per_hour: float
    average_earnings_per_km: float
    average_wait_time: float
    competition_level: int
    profitability_score: int
    driver_count: int
    ride_demand: int
    surge_multiplier: float
    predicted_demand_15m: float
    predicted_demand_30m: float
    predicted_demand_60m: float
    color_hex: str
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HotZoneListResponse(BaseModel):
    zones: List[HotZoneResponse]
    total: int
    updated_at: Optional[datetime] = None
