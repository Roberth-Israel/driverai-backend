from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.region import HotZone, Region
from app.ml.terrain_predictor import TerrainPredictor

router = APIRouter()
predictor = TerrainPredictor()


class CompactOffer(BaseModel):
    id: str
    bairro_origem: str
    bairro_destino: str
    distancia_km: float
    ganho_total: float
    ganho_por_km: float
    ganho_por_hora: float
    score_rentabilidade: int
    terreno_adequado: bool
    alerta_terreno: Optional[str] = None
    demanda_na_regiao: float
    tempo_espera_min: int


class CompactFeedResponse(BaseModel):
    offers: List[CompactOffer]
    total: int
    has_good_offers: bool


@router.get("/compact/feed", response_model=CompactFeedResponse)
async def get_compact_feed(
    lat: Optional[float] = None,
    lng: Optional[float] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    zones = db.query(HotZone).join(Region).filter(
        HotZone.is_active == 1
    ).order_by(desc(HotZone.profitability_score)).limit(limit).all()

    offers = []
    bairros = [
        "Centro", "Pinheiros", "Moema", "Vila Olímpia", "Itaim Bibi",
        "Perdizes", "Vila Madalena", "Aeroporto", "Shopping", "Berini",
        "Zona Norte", "Zona Sul", "Zona Leste", "Zona Oeste", "Barra Funda",
    ]

    for i, z in enumerate(zones[:limit]):
        o_idx = (i * 3) % len(bairros)
        d_idx = (o_idx + 1 + i) % len(bairros)
        if d_idx == o_idx:
            d_idx = (d_idx + 1) % len(bairros)

        dist = round(3 + (z.demand_intensity * 15), 1)
        ganho_km = round(2.0 + (z.average_earnings_per_km or 1.5), 2)
        ganho_total = round(dist * ganho_km, 2)
        ganho_hora = round(ganho_km * 20 + (z.surge_multiplier - 1) * 10, 0)

        terrain_result = predictor.predict(
            origem_lat=lat or -23.5505,
            origem_lng=lng or -46.6333,
            dest_lat=z.region.latitude,
            dest_lng=z.region.longitude,
        )

        offers.append(CompactOffer(
            id=str(z.id),
            bairro_origem=bairros[o_idx],
            bairro_destino=bairros[d_idx],
            distancia_km=dist,
            ganho_total=ganho_total,
            ganho_por_km=ganho_km,
            ganho_por_hora=ganho_hora,
            score_rentabilidade=z.profitability_score,
            terreno_adequado=terrain_result["adequado"],
            alerta_terreno=terrain_result["alerta"],
            demanda_na_regiao=z.demand_intensity,
            tempo_espera_min=max(1, int(z.average_wait_time)),
        ))

    has_good = any(o.score_rentabilidade >= 65 and o.terreno_adequado for o in offers)

    return CompactFeedResponse(offers=offers, total=len(offers), has_good_offers=has_good)


class EvaluateRideRequest(BaseModel):
    origem_lat: float
    origem_lng: float
    dest_lat: float
    dest_lng: float


@router.post("/compact/evaluate-ride", response_model=CompactOffer)
async def evaluate_ride(
    req: EvaluateRideRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    terrain = predictor.predict(req.origem_lat, req.origem_lng, req.dest_lat, req.dest_lng)
    dist = predictor._haversine(req.origem_lat, req.origem_lng, req.dest_lat, req.dest_lng)

    return CompactOffer(
        id="eval_1",
        bairro_origem="Origem",
        bairro_destino="Destino",
        distancia_km=round(dist, 1),
        ganho_total=0,
        ganho_por_km=0,
        ganho_por_hora=0,
        score_rentabilidade=80 if terrain["adequado"] else 45,
        terreno_adequado=terrain["adequado"],
        alerta_terreno=terrain["alerta"],
        demanda_na_regiao=0.6,
        tempo_espera_min=5,
    )
