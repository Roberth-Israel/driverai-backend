import uuid
from pydantic import BaseModel
from typing import Optional


class VehicleCreate(BaseModel):
    brand: str
    model: str
    year: int
    fuel_type: str
    fuel_consumption_km_per_liter: float
    fuel_price_per_liter: float = 5.5
    battery_capacity_kwh: Optional[float] = None
    energy_consumption_kwh_per_km: Optional[float] = None
    energy_price_per_kwh: Optional[float] = None


class VehicleResponse(BaseModel):
    id: uuid.UUID
    brand: str
    model: str
    year: int
    fuel_type: str
    fuel_consumption_km_per_liter: float
    fuel_price_per_liter: float
    cost_per_km: float
    battery_capacity_kwh: Optional[float] = None
    energy_consumption_kwh_per_km: Optional[float] = None
    energy_price_per_kwh: Optional[float] = None

    class Config:
        from_attributes = True
