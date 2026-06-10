from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from app.core.security import get_current_user
from app.models.user import User
from app.ml.terrain_predictor import TerrainPredictor

router = APIRouter()
predictor = TerrainPredictor()


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


@router.post("/terrain/predict", response_model=TerrainResponse)
async def predict_terrain(
    data: TerrainRequest,
    current_user: User = Depends(get_current_user),
):
    result = predictor.predict(
        origem_lat=data.origem_lat,
        origem_lng=data.origem_lng,
        dest_lat=data.dest_lat,
        dest_lng=data.dest_lng,
        vehicle_type=data.vehicle_type,
    )
    return TerrainResponse(**result)


@router.post("/terrain/route-check", response_model=dict)
async def check_route_terrain(
    data: TerrainRequest,
    current_user: User = Depends(get_current_user),
):
    result = predictor.predict(
        origem_lat=data.origem_lat,
        origem_lng=data.origem_lng,
        dest_lat=data.dest_lat,
        dest_lng=data.dest_lng,
        vehicle_type=data.vehicle_type,
    )

    segments = predictor.get_route_segments(
        origem_lat=data.origem_lat,
        origem_lng=data.origem_lng,
        dest_lat=data.dest_lat,
        dest_lng=data.dest_lng,
    )

    return {
        "overall": result,
        "segments": segments,
        "total_segments": len(segments),
        "warning_segments": sum(1 for s in segments if not s["adequado"]),
    }
