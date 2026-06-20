from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse

router = APIRouter()


@router.get("/vehicle", response_model=VehicleResponse)
async def get_vehicle(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vehicle = db.query(Vehicle).filter(Vehicle.user_id == current_user.id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não cadastrado")
    return _vehicle_to_response(vehicle)


@router.post("/vehicle", response_model=VehicleResponse)
async def save_vehicle(
    data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    vehicle = db.query(Vehicle).filter(Vehicle.user_id == current_user.id).first()

    if vehicle:
        vehicle.brand = data.brand
        vehicle.model = data.model
        vehicle.year = data.year
        vehicle.fuel_type = data.fuel_type
        vehicle.fuel_consumption_km_per_liter = data.fuel_consumption_km_per_liter
        vehicle.fuel_price_per_liter = data.fuel_price_per_liter
        vehicle.battery_capacity_kwh = data.battery_capacity_kwh
        vehicle.energy_consumption_kwh_per_km = data.energy_consumption_kwh_per_km
        vehicle.energy_price_per_kwh = data.energy_price_per_kwh
    else:
        vehicle = Vehicle(
            user_id=current_user.id,
            brand=data.brand,
            model=data.model,
            year=data.year,
            fuel_type=data.fuel_type,
            fuel_consumption_km_per_liter=data.fuel_consumption_km_per_liter,
            fuel_price_per_liter=data.fuel_price_per_liter,
            battery_capacity_kwh=data.battery_capacity_kwh,
            energy_consumption_kwh_per_km=data.energy_consumption_kwh_per_km,
            energy_price_per_kwh=data.energy_price_per_kwh,
        )
        db.add(vehicle)

    db.commit()
    db.refresh(vehicle)
    return _vehicle_to_response(vehicle)


def _vehicle_to_response(v: Vehicle) -> VehicleResponse:
    if v.fuel_type == "electric":
        cost_per_km = (v.energy_consumption_kwh_per_km or 0) * (v.energy_price_per_kwh or 0)
    else:
        cost_per_km = v.fuel_price_per_liter / v.fuel_consumption_km_per_liter if v.fuel_consumption_km_per_liter and v.fuel_consumption_km_per_liter > 0 else 0

    return VehicleResponse(
        id=str(v.id),
        brand=v.brand,
        model=v.model,
        year=v.year,
        fuel_type=v.fuel_type,
        fuel_consumption_km_per_liter=v.fuel_consumption_km_per_liter,
        fuel_price_per_liter=v.fuel_price_per_liter,
        cost_per_km=cost_per_km,
        battery_capacity_kwh=v.battery_capacity_kwh,
        energy_consumption_kwh_per_km=v.energy_consumption_kwh_per_km,
        energy_price_per_kwh=v.energy_price_per_kwh,
    )
