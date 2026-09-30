from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Dict, Any
from app.database import get_db
from app.models.models import User, Farm, Crop, PlantScan, Diagnosis, TreatmentSchedule

router = APIRouter(prefix="/admin", tags=["Admin Portal & System Stats"])

@router.get("/dashboard-stats")
async def get_admin_stats(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Calculates live platform telemetry dynamically from database records"""
    u_count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    c_count = (await db.execute(select(func.count(Crop.id)))).scalar() or 0
    s_count = (await db.execute(select(func.count(PlantScan.id)))).scalar() or 0
    d_count = (await db.execute(select(func.count(Diagnosis.id)))).scalar() or 0

    return {
        "total_users": u_count,
        "total_farmers": u_count,
        "total_crops": c_count,
        "total_scans": s_count,
        "ai_model_version": "AgriDoctor-Vision-v2.4",
        "active_diagnoses": d_count,
        "active_alerts_count": c_count
    }
