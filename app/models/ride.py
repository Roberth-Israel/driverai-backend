import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Ride(Base):
    __tablename__ = "rides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    origin_lat = Column(Float, nullable=False)
    origin_lng = Column(Float, nullable=False)
    dest_lat = Column(Float, nullable=False)
    dest_lng = Column(Float, nullable=False)
    origin_name = Column(String(200))
    destination_name = Column(String(200))
    distance_km = Column(Float, nullable=False)
    duration_minutes = Column(Float, nullable=False)
    fare = Column(Float, nullable=False)
    driver_earnings = Column(Float, nullable=False)
    fuel_cost = Column(Float, default=0.0)
    platform = Column(String(50))
    status = Column(String(20), default="completed")
    accepted = Column(Boolean, default=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"))
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
