from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.region import HotZone, Region
from app.schemas.assistant import ChatRequest, ChatResponse
from app.ml.chat_engine import ChatEngine

router = APIRouter()
chat_engine = ChatEngine()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    hot_zones = db.query(HotZone).join(Region).filter(
        HotZone.is_active == 1
    ).order_by(desc(HotZone.profitability_score)).limit(10).all()

    zones_data = [
        {
            "name": z.region.name,
            "score": z.profitability_score,
            "earnings_per_hour": z.average_earnings_per_hour,
            "wait_time": z.average_wait_time,
            "demand": z.demand_intensity,
            "predicted_15m": z.predicted_demand_15m,
            "predicted_30m": z.predicted_demand_30m,
            "predicted_60m": z.predicted_demand_60m,
            "competition": z.competition_level,
            "surge": z.surge_multiplier,
        }
        for z in hot_zones
    ]

    response = chat_engine.generate_response(
        message=data.message,
        context=data.context,
        zones=zones_data,
        user_name=current_user.name,
        user_earnings=current_user.total_earnings,
        user_rides=current_user.total_rides,
    )

    suggested = [
        {"name": z["name"], "score": z["score"]}
        for z in zones_data[:3]
    ]

    return ChatResponse(response=response, suggested_regions=suggested)
