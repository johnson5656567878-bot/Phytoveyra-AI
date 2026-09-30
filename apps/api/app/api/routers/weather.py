from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.models import Crop, PlantScan
from app.services.weather_service import WeatherService
from app.schemas.schemas import WeatherResponse, RiskAlertResponse

weather_router = APIRouter(prefix="/weather", tags=["Weather"])
alerts_router = APIRouter(prefix="/alerts", tags=["Disease & Pest Alerts"])

@weather_router.get("", response_model=WeatherResponse)
async def get_current_weather(location_name: str = "Coimbatore, Tamil Nadu"):
    return WeatherService.get_weather(location_name)

@alerts_router.get("", response_model=List[RiskAlertResponse])
async def get_risk_alerts(location_name: str = "Coimbatore, Tamil Nadu", db: AsyncSession = Depends(get_db)):
    # Query user's actual crops from database
    crop_res = await db.execute(select(Crop))
    user_crops = crop_res.scalars().all()

    if not user_crops:
        # Also check scans
        scan_res = await db.execute(select(PlantScan))
        scans = scan_res.scalars().all()
        if not scans:
            return []
        crop_names = list(set([s.crop_name for s in scans]))
    else:
        crop_names = list(set([c.name for c in user_crops]))

    # Calculate risk alerts ONLY for crops the user actually owns/scanned
    alerts = []
    weather = WeatherService.get_weather(location_name)
    humidity = weather["humidity_percent"]

    for idx, c_name in enumerate(crop_names):
        c_lower = c_name.lower()
        if "rice" in c_lower or "paddy" in c_lower:
            alerts.append({
                "id": f"alert-{idx}",
                "location_name": location_name,
                "crop_name": c_name,
                "disease_pest_name": "Stem Borer & Rice Blast Risk",
                "risk_level": "High Risk" if humidity > 80 else "Moderate",
                "reason": f"High atmospheric humidity ({humidity}%) in {location_name} increases spore germination risk for {c_name}.",
                "preventive_action": "Avoid over-fertilizing with nitrogen and maintain steady water level.",
                "created_at": "2026-09-27T10:00:00Z"
            })
        elif "chilli" in c_lower or "pepper" in c_lower:
            alerts.append({
                "id": f"alert-{idx}",
                "location_name": location_name,
                "crop_name": c_name,
                "disease_pest_name": "Chilli Leaf Curl Virus & Thrips",
                "risk_level": "Moderate",
                "reason": f"Warm weather conditions favor thrips vector activity in {c_name} fields.",
                "preventive_action": "Install yellow sticky traps and spray neem oil extract.",
                "created_at": "2026-09-27T10:00:00Z"
            })
        elif "tomato" in c_lower:
            alerts.append({
                "id": f"alert-{idx}",
                "location_name": location_name,
                "crop_name": c_name,
                "disease_pest_name": "Fungal Late Blight & Powdery Mildew",
                "risk_level": "High Risk" if humidity > 80 else "Moderate",
                "reason": f"Humidity levels above 80% create favorable incubation for {c_name} fungal spores.",
                "preventive_action": "Apply preventive copper hydroxide spray and ensure canopy drainage.",
                "created_at": "2026-09-27T10:00:00Z"
            })
        else:
            alerts.append({
                "id": f"alert-{idx}",
                "location_name": location_name,
                "crop_name": c_name,
                "disease_pest_name": f"Foliage Disease & Pest Warning for {c_name}",
                "risk_level": "Moderate",
                "reason": f"Weather conditions in {location_name} require routine monitoring for {c_name}.",
                "preventive_action": "Inspect leaf undersides weekly and maintain balanced irrigation.",
                "created_at": "2026-09-27T10:00:00Z"
            })

    return alerts

@alerts_router.delete("")
async def clear_all_alerts(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import delete
    from app.models.models import RiskAlert
    await db.execute(delete(RiskAlert))
    await db.commit()
    return {"message": "All disease and pest risk alerts cleared"}
