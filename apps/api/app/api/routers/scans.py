from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from typing import Optional, List
import uuid
import base64

from app.database import get_db
from app.models.models import PlantScan, Diagnosis, Crop
from app.schemas.schemas import ScanResponse, DiagnosisResponse
from app.services.ai_provider import RealVisionAIProvider

router = APIRouter(prefix="/scans", tags=["Plant Scans & AI Diagnosis"])
ai_provider = RealVisionAIProvider()

@router.post("/upload", response_model=ScanResponse)
async def upload_and_diagnose(
    file: Optional[UploadFile] = File(None),
    image_url: Optional[str] = Form(None),
    crop_id: Optional[str] = Form(None),
    crop_name: Optional[str] = Form("Auto-Detect"),
    notes: Optional[str] = Form(None),
    scan_type: Optional[str] = Form("initial"),
    db: AsyncSession = Depends(get_db)
):
    image_bytes = b""
    final_image_url = image_url

    if file:
        image_bytes = await file.read()
        b64_str = base64.b64encode(image_bytes).decode("utf-8")
        final_image_url = f"data:{file.content_type or 'image/png'};base64,{b64_str}"
    elif image_url and image_url.startswith("data:image"):
        try:
            header, encoded = image_url.split(",", 1)
            image_bytes = base64.b64decode(encoded)
        except Exception:
            pass

    if not image_bytes:
        raise HTTPException(status_code=400, detail="No plant photo uploaded")

    ai_result = await ai_provider.analyze_image(image_bytes, crop_name=crop_name or "Auto-Detect")

    identified_crop_name = ai_result.get("crop", crop_name if (crop_name and crop_name != "Auto-Detect") else "Unknown")
    
    linked_crop_id = crop_id
    if not linked_crop_id:
        c_res = await db.execute(select(Crop).where(Crop.name == identified_crop_name))
        existing_crop = c_res.scalars().first()
        if existing_crop:
            linked_crop_id = existing_crop.id
        else:
            new_crop = Crop(
                name=identified_crop_name,
                variety="Identified via AI Scan",
                area_acres=1.0,
                growth_stage="Vegetative Stage",
                health_status="Healthy" if ai_result["severity"] == "Healthy" else "Warning"
            )
            db.add(new_crop)
            await db.flush()
            linked_crop_id = new_crop.id

    scan = PlantScan(
        user_id="default-user-id",
        crop_id=linked_crop_id,
        crop_name=identified_crop_name,
        image_url=final_image_url,
        notes=notes,
        scan_type=scan_type or "initial"
    )
    db.add(scan)
    await db.flush()

    diagnosis = Diagnosis(
        scan_id=scan.id,
        class_id=ai_result.get("class_id"),
        full_class_name=ai_result.get("full_class_name"),
        condition_type=ai_result["condition_type"],
        title=ai_result["title"],
        confidence=ai_result["confidence"],
        severity=ai_result["severity"],
        symptoms=ai_result["symptoms"],
        causes=ai_result["causes"],
        heatmap_url=ai_result.get("heatmap_url"),
        explanation_reasoning=ai_result["explanation_reasoning"],
        is_low_confidence=ai_result["is_low_confidence"],
        recommended_next_step=ai_result["recommended_next_step"]
    )
    db.add(diagnosis)
    await db.commit()
    await db.refresh(scan)
    await db.refresh(diagnosis)

    return {
        "id": scan.id,
        "user_id": scan.user_id,
        "crop_id": scan.crop_id,
        "crop_name": scan.crop_name,
        "image_url": scan.image_url,
        "notes": scan.notes,
        "scan_type": scan.scan_type,
        "created_at": scan.created_at,
        "diagnosis": {
            "id": diagnosis.id,
            "scan_id": diagnosis.scan_id,
            "class_id": diagnosis.class_id,
            "full_class_name": diagnosis.full_class_name,
            "condition_type": diagnosis.condition_type,
            "title": diagnosis.title,
            "confidence": diagnosis.confidence,
            "severity": diagnosis.severity,
            "symptoms": diagnosis.symptoms,
            "causes": diagnosis.causes,
            "heatmap_url": diagnosis.heatmap_url,
            "explanation_reasoning": diagnosis.explanation_reasoning,
            "is_low_confidence": diagnosis.is_low_confidence,
            "recommended_next_step": diagnosis.recommended_next_step
        }
    }

@router.get("", response_model=List[ScanResponse])
async def list_scans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlantScan)
        .options(joinedload(PlantScan.diagnosis))
        .order_by(PlantScan.created_at.desc())
    )
    scans = result.scalars().unique().all()
    out = []
    for s in scans:
        out.append({
            "id": s.id,
            "user_id": s.user_id,
            "crop_id": s.crop_id,
            "crop_name": s.crop_name,
            "image_url": s.image_url,
            "notes": s.notes,
            "scan_type": s.scan_type,
            "created_at": s.created_at,
            "diagnosis": {
                "id": s.diagnosis.id,
                "scan_id": s.diagnosis.scan_id,
                "condition_type": s.diagnosis.condition_type,
                "title": s.diagnosis.title,
                "confidence": s.diagnosis.confidence,
                "severity": s.diagnosis.severity,
                "symptoms": s.diagnosis.symptoms,
                "causes": s.diagnosis.causes,
                "heatmap_url": s.diagnosis.heatmap_url,
                "explanation_reasoning": s.diagnosis.explanation_reasoning,
                "is_low_confidence": s.diagnosis.is_low_confidence,
                "recommended_next_step": s.diagnosis.recommended_next_step
            } if s.diagnosis else None
        })
    return out

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan_by_id(scan_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PlantScan)
        .options(joinedload(PlantScan.diagnosis))
        .where(PlantScan.id == scan_id)
    )
    scan = result.scalars().first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found")

    return {
        "id": scan.id,
        "user_id": scan.user_id,
        "crop_id": scan.crop_id,
        "crop_name": scan.crop_name,
        "image_url": scan.image_url,
        "notes": scan.notes,
        "scan_type": scan.scan_type,
        "created_at": scan.created_at,
        "diagnosis": {
            "id": scan.diagnosis.id,
            "scan_id": scan.diagnosis.scan_id,
            "condition_type": scan.diagnosis.condition_type,
            "title": scan.diagnosis.title,
            "confidence": scan.diagnosis.confidence,
            "severity": scan.diagnosis.severity,
            "symptoms": scan.diagnosis.symptoms,
            "causes": scan.diagnosis.causes,
            "heatmap_url": scan.diagnosis.heatmap_url,
            "explanation_reasoning": scan.diagnosis.explanation_reasoning,
            "is_low_confidence": scan.diagnosis.is_low_confidence,
            "recommended_next_step": scan.diagnosis.recommended_next_step
        } if scan.diagnosis else None
    }

@router.delete("")
async def clear_all_scans(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import delete
    from app.models.models import Treatment, RecoveryScan, TreatmentSchedule
    
    await db.execute(delete(RecoveryScan))
    await db.execute(delete(TreatmentSchedule))
    await db.execute(delete(Treatment))
    await db.execute(delete(Diagnosis))
    await db.execute(delete(PlantScan))
    await db.commit()
    return {"message": "All plant scan and diagnosis records have been cleared successfully"}
