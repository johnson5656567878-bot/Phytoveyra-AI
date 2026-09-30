import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database import engine, Base, AsyncSessionLocal
from app.seed import seed_initial_data

from app.api.routers.auth import router as auth_router
from app.api.routers.farms import farms_router, crops_router
from app.api.routers.scans import router as scans_router
from app.api.routers.treatments import treatments_router, schedules_router
from app.api.routers.recovery import router as recovery_router
from app.api.routers.weather import weather_router, alerts_router
from app.api.routers.fertilizer import router as fertilizer_router
from app.api.routers.experts import router as experts_router
from app.api.routers.chat import chat_router, voice_router
from app.api.routers.admin import router as admin_router

from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables & seed initial data
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Safe migration for new 38-class columns in SQLite
        try:
            await conn.execute(text("ALTER TABLE diagnoses ADD COLUMN class_id INTEGER;"))
        except Exception:
            pass
        try:
            await conn.execute(text("ALTER TABLE diagnoses ADD COLUMN full_class_name VARCHAR(255);"))
        except Exception:
            pass
    
    async with AsyncSessionLocal() as session:
        await seed_initial_data(session)

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multilingual AI Plant Health, Treatment & Recovery Platform Backend API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers under /api
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(farms_router, prefix=settings.API_V1_STR)
app.include_router(crops_router, prefix=settings.API_V1_STR)
app.include_router(scans_router, prefix=settings.API_V1_STR)
app.include_router(treatments_router, prefix=settings.API_V1_STR)
app.include_router(schedules_router, prefix=settings.API_V1_STR)
app.include_router(recovery_router, prefix=settings.API_V1_STR)
app.include_router(weather_router, prefix=settings.API_V1_STR)
app.include_router(alerts_router, prefix=settings.API_V1_STR)
app.include_router(fertilizer_router, prefix=settings.API_V1_STR)
app.include_router(experts_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(voice_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "demo_mode": settings.DEMO_MODE,
        "docs": f"{settings.API_V1_STR}/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
