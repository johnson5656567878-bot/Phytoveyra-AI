from fastapi import APIRouter
from app.schemas.schemas import FertilizerRequest, FertilizerResponse
from app.services.fertilizer_service import FertilizerService

router = APIRouter(prefix="/fertilizer", tags=["Fertilizer Calculator"])

@router.post("/calculate", response_model=FertilizerResponse)
async def calculate_fertilizer(req: FertilizerRequest):
    return FertilizerService.calculate(
        crop_name=req.crop_name,
        area_acres=req.area_acres,
        soil_n_ppm=req.soil_n_ppm or 20.0,
        soil_p_ppm=req.soil_p_ppm or 10.0,
        soil_k_ppm=req.soil_k_ppm or 150.0
    )
