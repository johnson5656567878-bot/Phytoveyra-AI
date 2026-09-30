from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# --- Auth & User ---
class UserRegister(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    preferred_language: Optional[str] = "en"
    phone_number: Optional[str] = None
    location_name: Optional[str] = "Coimbatore, Tamil Nadu"
    latitude: Optional[float] = 11.0168
    longitude: Optional[float] = 76.9558
    role_name: Optional[str] = "Farmer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role_name: str
    preferred_language: str
    phone_number: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# --- Farm & Crop ---
class FarmCreate(BaseModel):
    name: str
    location: str
    latitude: Optional[float] = 11.0168
    longitude: Optional[float] = 76.9558
    total_area_acres: float = 1.0
    soil_type: str = "Loamy Soil"
    irrigation_type: str = "Drip Irrigation"

class FarmResponse(BaseModel):
    id: str
    user_id: str
    name: str
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    total_area_acres: float
    soil_type: str
    irrigation_type: str

class CropCreate(BaseModel):
    farm_id: Optional[str] = None
    name: str
    variety: Optional[str] = None
    planting_date: Optional[str] = None
    area_acres: float = 1.0
    growth_stage: str = "Vegetative Stage"
    health_status: str = "Healthy"

class CropResponse(BaseModel):
    id: str
    farm_id: Optional[str]
    name: str
    variety: Optional[str]
    planting_date: Optional[str]
    area_acres: float
    growth_stage: str
    health_status: str
    created_at: datetime

# --- Scan & Diagnosis ---
class ScanCreate(BaseModel):
    crop_id: Optional[str] = None
    crop_name: Optional[str] = None
    image_url: str
    notes: Optional[str] = None
    scan_type: str = "initial"

class DiagnosisResponse(BaseModel):
    id: str
    scan_id: str
    class_id: Optional[int] = None
    full_class_name: Optional[str] = None
    condition_type: str
    title: str
    confidence: float
    severity: str
    symptoms: List[str]
    causes: List[str]
    heatmap_url: Optional[str] = None
    explanation_reasoning: Optional[str] = None
    is_low_confidence: bool
    recommended_next_step: Optional[str] = None

class ScanResponse(BaseModel):
    id: str
    user_id: str
    crop_id: Optional[str]
    crop_name: str
    image_url: str
    notes: Optional[str]
    scan_type: str
    created_at: datetime
    diagnosis: Optional[DiagnosisResponse] = None

# --- Treatment & Schedule ---
class TreatmentResponse(BaseModel):
    id: str
    diagnosis_id: str
    problem_title: str
    why_happening: str
    immediate_action: str
    cultural_control: Optional[str]
    biological_organic: Optional[str]
    approved_chemical: Optional[str]
    safety_warning: Optional[str]
    follow_up_days: int
    source_reference: str

class ScheduleCreate(BaseModel):
    crop_id: Optional[str] = None
    scan_id: Optional[str] = None
    treatment_id: Optional[str] = None
    action_item: str
    scheduled_date: str
    follow_up_date: str
    notes: Optional[str] = None

class ScheduleResponse(BaseModel):
    id: str
    crop_id: Optional[str]
    scan_id: Optional[str]
    treatment_id: Optional[str]
    action_item: str
    scheduled_date: str
    follow_up_date: str
    status: str
    notes: Optional[str]

# --- Recovery ---
class RecoveryCreate(BaseModel):
    schedule_id: Optional[str] = None
    original_scan_id: str
    followup_image_url: str
    notes: Optional[str] = None

class RecoveryResponse(BaseModel):
    id: str
    schedule_id: Optional[str]
    original_scan_id: str
    followup_image_url: str
    initial_severity: str
    current_severity: str
    improvement_percentage: Optional[float]
    recovery_status: str
    analysis_notes: Optional[str]
    initial_image_url: str

# --- Weather & Risk ---
class WeatherResponse(BaseModel):
    location_name: str
    temperature_c: float
    humidity_percent: float
    rainfall_mm: float
    wind_speed_kmh: float
    forecast_text: str
    warning: Optional[str]

class RiskAlertResponse(BaseModel):
    id: str
    location_name: str
    crop_name: str
    disease_pest_name: str
    risk_level: str
    reason: str
    preventive_action: str
    created_at: datetime

# --- Fertilizer Calculator ---
class FertilizerRequest(BaseModel):
    crop_name: str
    area_acres: float
    soil_n_ppm: Optional[float] = 20.0
    soil_p_ppm: Optional[float] = 10.0
    soil_k_ppm: Optional[float] = 150.0
    growth_stage: Optional[str] = "Vegetative Stage"

class FertilizerResponse(BaseModel):
    crop_name: str
    area_acres: float
    nitrogen_req_kg: float
    phosphorus_req_kg: float
    potassium_req_kg: float
    recommended_urea_kg: float
    recommended_dap_kg: float
    recommended_mop_kg: float
    organic_compost_tons: float
    formula_explanation: str

# --- Expert Support ---
class ExpertRequestCreate(BaseModel):
    crop_name: str
    image_url: Optional[str] = None
    question: str

class ExpertAnswerCreate(BaseModel):
    request_id: str
    response_text: str
    recommended_action: Optional[str] = None

# --- Chat & RAG ---
class ChatMessageCreate(BaseModel):
    session_id: Optional[str] = None
    text: str
    image_url: Optional[str] = None
    voice_url: Optional[str] = None
    language: Optional[str] = "en"
    history: Optional[List[dict]] = None

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    sender: str
    text: str
    image_url: Optional[str] = None
    citations: List[str] = []
    created_at: datetime
