from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import AlertResponse, AlertListResponse

router = APIRouter()


@router.get("/alerts", response_model=AlertListResponse)
async def get_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id,
    ).order_by(desc(Alert.created_at)).limit(50).all()

    unread = sum(1 for a in alerts if not a.read)

    return AlertListResponse(
        alerts=[
            AlertResponse(
                id=str(a.id),
                title=a.title,
                message=a.message,
                type=a.type,
                severity=a.severity,
                read=a.read,
                created_at=a.created_at,
            )
            for a in alerts
        ],
        unread_count=unread,
    )


@router.post("/alerts/{alert_id}/read")
async def mark_as_read(
    alert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id,
        Alert.user_id == current_user.id,
    ).first()
    if alert:
        alert.read = True
        db.commit()
    return {"status": "ok"}
