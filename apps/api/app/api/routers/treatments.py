from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.database import get_db
from app.models.models import TreatmentSchedule, PlantScan, Diagnosis
from app.schemas.schemas import TreatmentResponse, ScheduleCreate, ScheduleResponse
from app.services.treatment_service import TreatmentService

treatments_router = APIRouter(prefix="/treatments", tags=["Treatments"])
schedules_router = APIRouter(prefix="/schedules", tags=["Schedules"])

@treatments_router.get("/recommend")
async def get_recommendation(
    diagnosis_title: str,
    crop_name: Optional[str] = "Unknown",
    condition_type: Optional[str] = "unknown",
    severity: Optional[str] = "Moderate"
):
    rec = TreatmentService.get_recommendation(
        crop_name=crop_name,
        diagnosis_title=diagnosis_title,
        condition_type=condition_type,
        severity=severity,
        is_low_confidence=False,
        confidence=0.85
    )
    return {
        "id": "treat-rec-dynamic",
        "diagnosis_id": "diag-dynamic",
        **rec
    }

async def fetch_scan_treatment(scan_id: str, db: AsyncSession):
    scan_res = await db.execute(select(PlantScan).where(PlantScan.id == scan_id))
    scan = scan_res.scalars().first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found")

    diag_res = await db.execute(select(Diagnosis).where(Diagnosis.scan_id == scan.id))
    diag = diag_res.scalars().first()

    crop_name = scan.crop_name if scan.crop_name and scan.crop_name not in ["Detected Crop", "Auto-Detect"] else "Unknown"
    
    full_class_name = diag.full_class_name if diag and diag.full_class_name else "Unknown"
    title = diag.title if diag else "Plant Condition"
    condition_type = diag.condition_type if diag else "unknown"
    severity = diag.severity if diag else "Uncertain"
    confidence = diag.confidence if diag else 0.0
    is_low_confidence = diag.is_low_confidence if diag else False
    class_id = diag.class_id if diag else None

    rec = TreatmentService.get_recommendation(
        full_class_name=full_class_name,
        crop_name=crop_name,
        diagnosis_title=title,
        condition_type=condition_type,
        severity=severity,
        is_low_confidence=is_low_confidence,
        confidence=confidence
    )

    return {
        "scan_id": scan.id,
        "class_id": class_id,
        "full_class_name": full_class_name,
        "crop_name": crop_name,
        "image_url": scan.image_url,
        "created_at": scan.created_at,
        "diagnosis_title": title,
        "severity": severity,
        "confidence": confidence,
        "symptoms": diag.symptoms if diag else [],
        "causes": diag.causes if diag else [],
        "is_low_confidence": is_low_confidence,
        "treatment": {
            "id": f"treat-{scan.id}",
            "diagnosis_id": diag.id if diag else scan.id,
            **rec
        }
    }

@treatments_router.get("/by-scan/{scan_id}")
async def get_treatment_by_scan_id_legacy(scan_id: str, db: AsyncSession = Depends(get_db)):
    return await fetch_scan_treatment(scan_id, db)

@treatments_router.get("/{scan_id}")
async def get_treatment_by_scan_id(scan_id: str, db: AsyncSession = Depends(get_db)):
    return await fetch_scan_treatment(scan_id, db)

@schedules_router.get("", response_model=List[ScheduleResponse])
async def list_schedules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TreatmentSchedule).order_by(TreatmentSchedule.created_at.desc()))
    schedules = result.scalars().all()
    return schedules

@schedules_router.post("", response_model=ScheduleResponse)
async def create_schedule(sched_in: ScheduleCreate, db: AsyncSession = Depends(get_db)):
    schedule = TreatmentSchedule(
        user_id="default-user-id",
        crop_id=sched_in.crop_id,
        scan_id=sched_in.scan_id,
        treatment_id=sched_in.treatment_id,
        action_item=sched_in.action_item,
        scheduled_date=sched_in.scheduled_date,
        follow_up_date=sched_in.follow_up_date,
        status="Pending",
        notes=sched_in.notes
    )
    db.add(schedule)
    await db.commit()
    await db.refresh(schedule)
    return schedule

@schedules_router.patch("/{schedule_id}/status")
async def update_schedule_status(schedule_id: str, status: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TreatmentSchedule).where(TreatmentSchedule.id == schedule_id))
    schedule = result.scalars().first()
    if schedule:
        schedule.status = status
        await db.commit()
        return {"message": "Status updated successfully", "status": status}
    raise HTTPException(status_code=404, detail="Schedule not found")
