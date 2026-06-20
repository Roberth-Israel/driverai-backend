from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.region import HotZone, Region
from app.schemas.hotzone import HotZoneListResponse, HotZoneResponse

router = APIRouter()


@router.get("/hot-zones", response_model=HotZoneListResponse)
async def get_hot_zones(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    radius: Optional[float] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(HotZone).join(Region).filter(HotZone.is_active == 1)

    if lat and lng and radius:
        query = query.filter(
            Region.latitude.between(lat - radius, lat + radius),
            Region.longitude.between(lng - radius, lng + radius),
        )

    zones = query.order_by(desc(HotZone.profitability_score)).limit(50).all()

    result = []
    for z in zones:
        result.append(HotZoneResponse(
            id=str(z.id),
            name=z.region.name,
            latitude=z.region.latitude,
            longitude=z.region.longitude,
            demand_intensity=z.demand_intensity,
            average_earnings_per_hour=z.average_earnings_per_hour,
            average_earnings_per_km=z.average_earnings_per_km,
            average_wait_time=z.average_wait_time,
            competition_level=z.competition_level,
            profitability_score=z.profitability_score,
            driver_count=z.driver_count,
            ride_demand=z.ride_demand,
            surge_multiplier=z.surge_multiplier,
            predicted_demand_15m=z.predicted_demand_15m,
            predicted_demand_30m=z.predicted_demand_30m,
            predicted_demand_60m=z.predicted_demand_60m,
            color_hex=_get_score_color(z.profitability_score),
            updated_at=z.updated_at,
        ))

    return HotZoneListResponse(
        zones=result,
        total=len(result),
        updated_at=zones[0].updated_at if zones else None,
    )


def _get_score_color(score: int) -> str:
    if score >= 80: return "#4CAF50"
    if score >= 60: return "#8BC34A"
    if score >= 40: return "#FFC107"
    if score >= 20: return "#FF9800"
    return "#F44336"
