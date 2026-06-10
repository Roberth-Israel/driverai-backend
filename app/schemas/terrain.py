from pydantic import BaseModel
from typing import Optional, List


class TerrainRequest(BaseModel):
    origem_lat: float
    origem_lng: float
    dest_lat: float
    dest_lng: float
    vehicle_type: str = "sedan"


class TerrainResponse(BaseModel):
    adequado: bool
    confidence: float
    alerta: Optional[str] = None
    tipo_terreno: str
    impact_score: float
    recomendacao: str
    elevation_change_m: Optional[float] = None
    roughness_index: Optional[float] = None
    surface_type: Optional[str] = None
    vehicle_factor: Optional[float] = None


class RouteSegment(BaseModel):
    segment: int
    adequado: bool
    tipo_terreno: str
    impact_score: float
    alerta: Optional[str] = None


class RouteCheckResponse(BaseModel):
    overall: TerrainResponse
    segments: List[RouteSegment]
    total_segments: int
    warning_segments: int
