from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.region import HotZone, Region
from app.schemas.ranking import RankingResponse, RankingRegion

router = APIRouter()

VALID_SORT = ["profitability", "demand", "distance", "earnings"]


@router.get("/ranking", response_model=RankingResponse)
async def get_ranking(
    sort_by: str = Query("profitability"),
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if sort_by not in VALID_SORT:
        raise HTTPException(status_code=400, detail=f"sort_by inválido. Opções: {VALID_SORT}")

    query = db.query(HotZone).join(Region).filter(HotZone.is_active == 1)

    sort_map = {
        "profitability": desc(HotZone.profitability_score),
        "demand": desc(HotZone.demand_intensity),
        "distance": asc(HotZone.demand_intensity),
        "earnings": desc(HotZone.average_earnings_per_hour),
    }
    query = query.order_by(sort_map[sort_by])

    zones = query.limit(50).all()

    regions = []
    for z in zones:
        regions.append(RankingRegion(
            id=str(z.id),
            name=z.region.name,
            latitude=z.region.latitude,
            longitude=z.region.longitude,
            demand_intensity=z.demand_intensity,
            average_earnings_per_hour=z.average_earnings_per_hour,
            average_earnings_per_km=z.average_earnings_per_km,
            average_wait_time=z.average_wait_time,
            distance_to_region=0,
            competition_level=z.competition_level,
            profitability_score=z.profitability_score,
            color_hex=_get_score_color(z.profitability_score),
        ))

    return RankingResponse(regions=regions, total=len(regions))


def _get_score_color(score: int) -> str:
    if score >= 80: return "#4CAF50"
    if score >= 60: return "#8BC34A"
    if score >= 40: return "#FFC107"
    if score >= 20: return "#FF9800"
    return "#F44336"
