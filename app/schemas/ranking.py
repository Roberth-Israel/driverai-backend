import uuid
from pydantic import BaseModel
from typing import List, Optional


class RankingRegion(BaseModel):
    id: uuid.UUID
    name: str
    latitude: float
    longitude: float
    demand_intensity: float
    average_earnings_per_hour: float
    average_earnings_per_km: float
    average_wait_time: float
    distance_to_region: float
    competition_level: int
    profitability_score: int
    color_hex: str


class RankingResponse(BaseModel):
    regions: List[RankingRegion]
    total: int
