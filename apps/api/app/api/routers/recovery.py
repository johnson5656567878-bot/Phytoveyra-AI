from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import base64
from app.database import get_db
from app.models.models import RecoveryScan, PlantScan, Diagnosis
from app.schemas.schemas import RecoveryResponse
from app.services.recovery_service import RecoveryService

router = APIRouter(prefix="/recovery", tags=["Recovery Monitoring & Before/After"])

@router.get("/by-scan/{scan_id}")
async def get_recovery_by_scan_id(scan_id: str, db: AsyncSession = Depends(get_db)):
    scan_res = await db.execute(select(PlantScan).where(PlantScan.id == scan_id))
    scan = scan_res.scalars().first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found")

    diag_res = await db.execute(select(Diagnosis).where(Diagnosis.scan_id == scan.id))
    diag = diag_res.scalars().first()

    rec_res = await db.execute(select(RecoveryScan).where(RecoveryScan.original_scan_id == scan.id).order_by(RecoveryScan.created_at.desc()))
    recovery = rec_res.scalars().first()

    return {
        "scan_id": scan.id,
        "crop_name": scan.crop_name,
        "initial_image_url": scan.image_url,
        "initial_date": scan.created_at,
        "initial_severity": diag.severity if diag else "Severe",
        "has_followup": True if recovery else False,
        "recovery": {
            "id": recovery.id,
            "original_scan_id": recovery.original_scan_id,
            "followup_image_url": recovery.followup_image_url,
            "initial_severity": recovery.initial_severity,
            "current_severity": recovery.current_severity,
            "improvement_percentage": recovery.improvement_percentage,
            "recovery_status": recovery.recovery_status,
            "analysis_notes": recovery.analysis_notes,
            "created_at": recovery.created_at
        } if recovery else None
    }

@router.post("/upload", response_model=RecoveryResponse)
async def upload_recovery_scan(
    original_scan_id: str = Form(...),
    file: Optional[UploadFile] = File(None),
    followup_image_url: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    scan_res = await db.execute(select(PlantScan).where(PlantScan.id == original_scan_id))
    original_scan = scan_res.scalars().first()
    if not original_scan:
        raise HTTPException(status_code=404, detail="Original scan not found")

    diag_res = await db.execute(select(Diagnosis).where(Diagnosis.scan_id == original_scan.id))
    diag = diag_res.scalars().first()
    initial_severity = diag.severity if diag else "Severe"

    final_follow_up_url = followup_image_url
    if file:
        content = await file.read()
        b64 = base64.b64encode(content).decode("utf-8")
        final_follow_up_url = f"data:{file.content_type or 'image/png'};base64,{b64}"

    if not final_follow_up_url:
        raise HTTPException(status_code=400, detail="Follow-up image is required")

    res = RecoveryService.analyze_recovery(initial_severity=initial_severity, follow_up_notes=notes or "")

    recovery = RecoveryScan(
        user_id="default-user-id",
        original_scan_id=original_scan.id,
        followup_image_url=final_follow_up_url,
        initial_severity=initial_severity,
        current_severity=res["current_severity"],
        improvement_percentage=res["improvement_percentage"],
        recovery_status=res["recovery_status"],
        analysis_notes=res["analysis_notes"]
    )
    db.add(recovery)
    await db.commit()
    await db.refresh(recovery)

    return {
        "id": recovery.id,
        "schedule_id": recovery.schedule_id,
        "original_scan_id": recovery.original_scan_id,
        "followup_image_url": recovery.followup_image_url,
        "initial_severity": recovery.initial_severity,
        "current_severity": recovery.current_severity,
        "improvement_percentage": recovery.improvement_percentage,
        "recovery_status": recovery.recovery_status,
        "analysis_notes": recovery.analysis_notes,
        "initial_image_url": original_scan.image_url
    }

@router.get("", response_model=List[RecoveryResponse])
async def list_recovery_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RecoveryScan).order_by(RecoveryScan.created_at.desc()))
    records = result.scalars().all()
    out = []
    for r in records:
        orig_res = await db.execute(select(PlantScan).where(PlantScan.id == r.original_scan_id))
        orig = orig_res.scalars().first()
        out.append({
            "id": r.id,
            "schedule_id": r.schedule_id,
            "original_scan_id": r.original_scan_id,
            "followup_image_url": r.followup_image_url,
            "initial_severity": r.initial_severity,
            "current_severity": r.current_severity,
            "improvement_percentage": r.improvement_percentage,
            "recovery_status": r.recovery_status,
            "analysis_notes": r.analysis_notes,
            "initial_image_url": orig.image_url if orig else ""
        })
    return out
