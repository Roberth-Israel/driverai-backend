from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, hotzones, ranking, assistant, dashboard, vehicle, alerts, admin, terrain, compact, update

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DriverAI Pro API",
    description="API do copiloto inteligente para motoristas de aplicativo",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticação"])
app.include_router(hotzones.router, prefix="/api/v1", tags=["Zonas Quentes"])
app.include_router(ranking.router, prefix="/api/v1", tags=["Ranking"])
app.include_router(assistant.router, prefix="/api/v1/assistant", tags=["Assistente IA"])
app.include_router(dashboard.router, prefix="/api/v1", tags=["Dashboard"])
app.include_router(vehicle.router, prefix="/api/v1", tags=["Veículo"])
app.include_router(alerts.router, prefix="/api/v1", tags=["Alertas"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(terrain.router, prefix="/api/v1", tags=["Terreno"])
app.include_router(compact.router, prefix="/api/v1", tags=["Compacto"])
app.include_router(update.router, prefix="/api/v1", tags=["Update"])

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0", "service": "DriverAI Pro"}
