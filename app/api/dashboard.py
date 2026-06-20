from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.ride import Ride
from app.schemas.dashboard import DashboardResponse, RideSummary

router = APIRouter()


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    period: str = Query("week", enum=["day", "week", "month"]),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    now = datetime.utcnow()

    if period == "day":
        display_since = now - timedelta(days=1)
    elif period == "week":
        display_since = now - timedelta(weeks=1)
    else:
        display_since = now - timedelta(days=30)

    base_query = db.query(Ride).filter(
        Ride.user_id == current_user.id,
        Ride.status == "completed",
    )

    all_rides = base_query.filter(Ride.created_at >= now - timedelta(days=30)).all()

    display_rides = [r for r in all_rides if r.created_at >= display_since]

    daily_rides = [r for r in all_rides if r.created_at >= now - timedelta(days=1)]
    weekly_rides = [r for r in all_rides if r.created_at >= now - timedelta(weeks=1)]
    monthly_rides = [r for r in all_rides if r.created_at >= now - timedelta(days=30)]

    total_earnings = sum(r.driver_earnings for r in display_rides)
    total_fuel = sum(r.fuel_cost for r in display_rides)
    total_distance = sum(r.distance_km for r in display_rides)
    total_duration = sum(r.duration_minutes for r in display_rides)
    accepted = sum(1 for r in display_rides if r.accepted)
    rejected = sum(1 for r in display_rides if not r.accepted)

    recent = base_query.order_by(desc(Ride.created_at)).limit(20).all()

    return DashboardResponse(
        daily_earnings=sum(r.driver_earnings for r in daily_rides),
        weekly_earnings=sum(r.driver_earnings for r in weekly_rides),
        monthly_earnings=sum(r.driver_earnings for r in monthly_rides),
        net_profit=total_earnings - total_fuel,
        fuel_cost=total_fuel,
        energy_cost=0,
        avg_per_hour=total_earnings / (total_duration / 60) if total_duration > 0 else 0,
        avg_per_km=total_earnings / total_distance if total_distance > 0 else 0,
        total_rides=len(display_rides),
        accepted_rides=accepted,
        rejected_rides=rejected,
        avg_rating=current_user.avg_rating,
        recent_rides=[
            RideSummary(
                id=str(r.id),
                origin=r.origin_name or "Origem",
                destination=r.destination_name or "Destino",
                distance=r.distance_km,
                fare=r.fare,
                driver_earnings=r.driver_earnings,
                status=r.status,
                created_at=r.created_at,
            )
            for r in recent
        ],
    )
