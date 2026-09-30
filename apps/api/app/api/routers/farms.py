from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.models import Farm, Crop
from app.schemas.schemas import FarmCreate, FarmResponse, CropCreate, CropResponse

farms_router = APIRouter(prefix="/farms", tags=["Farms"])
crops_router = APIRouter(prefix="/crops", tags=["Crops"])

# --- Farms ---
@farms_router.get("", response_model=List[FarmResponse])
async def list_farms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farm))
    farms = result.scalars().all()
    return farms

@farms_router.post("", response_model=FarmResponse)
async def create_farm(farm_in: FarmCreate, db: AsyncSession = Depends(get_db)):
    farm = Farm(
        user_id="default-user-id",
        name=farm_in.name,
        location=farm_in.location,
        latitude=farm_in.latitude,
        longitude=farm_in.longitude,
        total_area_acres=farm_in.total_area_acres,
        soil_type=farm_in.soil_type,
        irrigation_type=farm_in.irrigation_type
    )
    db.add(farm)
    await db.commit()
    await db.refresh(farm)
    return farm

# --- Crops ---
@crops_router.get("", response_model=List[CropResponse])
async def list_crops(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Crop).order_by(Crop.created_at.desc()))
    crops = result.scalars().all()
    return crops

@crops_router.post("", response_model=CropResponse)
async def create_crop(crop_in: CropCreate, db: AsyncSession = Depends(get_db)):
    crop = Crop(
        user_id="default-user-id",
        farm_id=crop_in.farm_id,
        name=crop_in.name,
        variety=crop_in.variety,
        planting_date=crop_in.planting_date,
        area_acres=crop_in.area_acres,
        growth_stage=crop_in.growth_stage,
        health_status=crop_in.health_status
    )
    db.add(crop)
    await db.commit()
    await db.refresh(crop)
    return crop
