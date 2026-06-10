import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class DriverProfile(Base):
    __tablename__ = "driver_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True)
    preferred_regions = Column(Text)
    preferred_hours_start = Column(Integer, default=6)
    preferred_hours_end = Column(Integer, default=22)
    preferred_ride_distance_min = Column(Float, default=2.0)
    preferred_ride_distance_max = Column(Float, default=30.0)
    acceptance_rate = Column(Float, default=1.0)
    rejection_rate = Column(Float, default=0.0)
    avg_earnings_per_hour = Column(Float, default=0.0)
    avg_earnings_per_km = Column(Float, default=0.0)
    preferred_platforms = Column(String(200))
    learning_version = Column(Integer, default=1)
    embedding_vector = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DriverPreference(Base):
    __tablename__ = "driver_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Text)
    weight = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
