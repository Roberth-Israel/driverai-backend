from typing import Optional
from app.models.alert import Alert
from app.core.database import SessionLocal


class NotificationService:
    async def send_zone_heating_alert(self, user_id: str, zone_name: str, score: int):
        await self._create_alert(
            user_id=user_id,
            title="🔥 Região aquecendo!",
            message=f"A região {zone_name} está com demanda crescente. Score: {score}/100",
            type="zone_heating",
            severity="high" if score >= 80 else "medium",
        )

    async def send_surge_alert(self, user_id: str, zone_name: str, multiplier: float):
        await self._create_alert(
            user_id=user_id,
            title="⚡ Tarifa Dinâmica!",
            message=f"Tarifa dinâmica {multiplier}x detectada em {zone_name}",
            type="surge_pricing",
            severity="high",
        )

    async def send_event_alert(self, user_id: str, event_name: str, zone_name: str):
        await self._create_alert(
            user_id=user_id,
            title="🎉 Evento Gerando Demanda",
            message=f"{event_name} em {zone_name} está gerando alta procura por corridas",
            type="event",
            severity="medium",
        )

    async def send_earning_opportunity(self, user_id: str, zone_name: str, amount: float):
        await self._create_alert(
            user_id=user_id,
            title="💰 Oportunidade de Ganho",
            message=f"Demanda alta em {zone_name} — ganho estimado: R$ {amount:.2f}",
            type="opportunity",
            severity="high",
        )

    async def _create_alert(self, user_id: str, title: str, message: str, type: str, severity: str):
        db = SessionLocal()
        try:
            alert = Alert(
                user_id=user_id,
                title=title,
                message=message,
                type=type,
                severity=severity,
            )
            db.add(alert)
            db.commit()
        finally:
            db.close()

notification_service = NotificationService()
