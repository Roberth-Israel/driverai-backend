from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.ride import Ride
from app.models.region import HotZone

router = APIRouter()


@router.get("/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")

    total_users = db.query(func.count(User.id)).scalar()
    total_rides = db.query(func.count(Ride.id)).scalar()
    total_earnings = db.query(func.sum(Ride.driver_earnings)).scalar() or 0
    active_zones = db.query(func.count(HotZone.id)).filter(HotZone.is_active == 1).scalar()

    return {
        "total_users": total_users,
        "total_rides": total_rides,
        "total_earnings": float(total_earnings),
        "active_zones": active_zones,
        "period": "all_time",
    }


@router.get("/stats/daily")
async def get_daily_stats(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")

    since = datetime.utcnow() - timedelta(days=days)
    daily_stats = (
        db.query(
            func.date(Ride.created_at).label("date"),
            func.count(Ride.id).label("rides"),
            func.sum(Ride.driver_earnings).label("earnings"),
        )
        .filter(Ride.created_at >= since)
        .group_by(func.date(Ride.created_at))
        .order_by(func.date(Ride.created_at))
        .all()
    )

    return [
        {
            "date": str(row.date),
            "rides": row.rides,
            "earnings": float(row.earnings or 0),
        }
        for row in daily_stats
    ]
