import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Region(Base):
    __tablename__ = "regions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    state = Column(String(50))
    city = Column(String(100))
    population_density = Column(Float, default=0.0)
    commercial_density = Column(Float, default=0.0)
    has_airport = Column(Integer, default=0)
    has_bus_station = Column(Integer, default=0)
    has_mall = Column(Integer, default=0)
    has_university = Column(Integer, default=0)
    has_hospital = Column(Integer, default=0)
    has_business_center = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class HotZone(Base):
    __tablename__ = "hot_zones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=False)
    region = relationship("Region", backref="hot_zones")
    demand_intensity = Column(Float, default=0.0)
    average_earnings_per_hour = Column(Float, default=0.0)
    average_earnings_per_km = Column(Float, default=0.0)
    average_wait_time = Column(Float, default=0.0)
    competition_level = Column(Integer, default=0)
    profitability_score = Column(Integer, default=0)
    driver_count = Column(Integer, default=0)
    ride_demand = Column(Integer, default=0)
    weather_condition = Column(String(50))
    traffic_level = Column(Integer, default=0)
    surge_multiplier = Column(Float, default=1.0)
    predicted_demand_15m = Column(Float, default=0.0)
    predicted_demand_30m = Column(Float, default=0.0)
    predicted_demand_60m = Column(Float, default=0.0)
    is_active = Column(Integer, default=1)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
