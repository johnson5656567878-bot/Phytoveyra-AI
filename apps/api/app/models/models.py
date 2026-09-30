import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Role(Base):
    __tablename__ = "roles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False) # Farmer, Expert, Admin
    description = Column(String(255), nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_name = Column(String(50), default="Farmer")
    preferred_language = Column(String(10), default="en") # en, ta, hi, te, ml, kn
    phone_number = Column(String(50), nullable=True)
    location_name = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True)

    farms = relationship("Farm", back_populates="owner")
    scans = relationship("PlantScan", back_populates="user")
    expert_requests = relationship("ExpertRequest", back_populates="farmer")

class Farm(Base):
    __tablename__ = "farms"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    total_area_acres = Column(Float, default=1.0)
    soil_type = Column(String(100), default="Loamy Soil")
    irrigation_type = Column(String(100), default="Drip Irrigation")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="farms")
    crops = relationship("Crop", back_populates="farm")

class Crop(Base):
    __tablename__ = "crops"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    farm_id = Column(String(36), ForeignKey("farms.id"), nullable=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    name = Column(String(255), nullable=False) # e.g. Tomato, Rice, Wheat, Chilli, Corn
    variety = Column(String(255), nullable=True)
    planting_date = Column(String(50), nullable=True)
    area_acres = Column(Float, default=1.0)
    growth_stage = Column(String(100), default="Vegetative Stage")
    health_status = Column(String(50), default="Healthy")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    farm = relationship("Farm", back_populates="crops")
    scans = relationship("PlantScan", back_populates="crop")
    schedules = relationship("TreatmentSchedule", back_populates="crop")

class PlantScan(Base):
    __tablename__ = "plant_scans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, default="default-user-id")
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=True)
    crop_name = Column(String(255), nullable=False, default="Unknown")
    image_url = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    scan_type = Column(String(50), default="initial")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="scans")
    crop = relationship("Crop", back_populates="scans")
    diagnosis = relationship("Diagnosis", back_populates="scan", uselist=False)

class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    scan_id = Column(String(36), ForeignKey("plant_scans.id"), nullable=False, unique=True)
    class_id = Column(Integer, nullable=True)
    full_class_name = Column(String(255), nullable=True)
    condition_type = Column(String(50), nullable=False) # disease, pest, nutrient_deficiency, healthy, unknown
    title = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False) # Mild, Moderate, Severe, Critical, Healthy, Uncertain
    symptoms = Column(JSON, default=list)
    causes = Column(JSON, default=list)
    heatmap_url = Column(Text, nullable=True)
    explanation_reasoning = Column(Text, nullable=True)
    is_low_confidence = Column(Boolean, default=False)
    recommended_next_step = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    scan = relationship("PlantScan", back_populates="diagnosis")
    treatment = relationship("Treatment", back_populates="diagnosis", uselist=False)

class Treatment(Base):
    __tablename__ = "treatments"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    diagnosis_id = Column(String(36), ForeignKey("diagnoses.id"), nullable=False, unique=True)
    problem_title = Column(String(255), nullable=False)
    why_happening = Column(Text, nullable=False)
    immediate_action = Column(Text, nullable=False)
    cultural_control = Column(Text, nullable=True)
    biological_organic = Column(Text, nullable=True)
    approved_chemical = Column(Text, nullable=True)
    safety_warning = Column(Text, nullable=True)
    follow_up_days = Column(Integer, default=7)
    source_reference = Column(String(255), default="Verified Extension Knowledge Base")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    diagnosis = relationship("Diagnosis", back_populates="treatment")
    schedules = relationship("TreatmentSchedule", back_populates="treatment")

class TreatmentSchedule(Base):
    __tablename__ = "treatment_schedules"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, default="default-user-id")
    crop_id = Column(String(36), ForeignKey("crops.id"), nullable=True)
    scan_id = Column(String(36), ForeignKey("plant_scans.id"), nullable=True)
    treatment_id = Column(String(36), ForeignKey("treatments.id"), nullable=True)
    action_item = Column(String(255), nullable=False)
    scheduled_date = Column(String(50), nullable=False)
    follow_up_date = Column(String(50), nullable=False)
    status = Column(String(50), default="Pending") # Pending, Completed, Rescheduled, Cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    crop = relationship("Crop", back_populates="schedules")
    treatment = relationship("Treatment", back_populates="schedules")
    recovery_scans = relationship("RecoveryScan", back_populates="schedule")

class RecoveryScan(Base):
    __tablename__ = "recovery_scans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, default="default-user-id")
    schedule_id = Column(String(36), ForeignKey("treatment_schedules.id"), nullable=True)
    original_scan_id = Column(String(36), ForeignKey("plant_scans.id"), nullable=False)
    followup_image_url = Column(Text, nullable=False)
    initial_severity = Column(String(50), nullable=False)
    current_severity = Column(String(50), nullable=False)
    improvement_percentage = Column(Float, nullable=True)
    recovery_status = Column(String(50), nullable=False) # Improving, Stable, Worsening, Uncertain
    analysis_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    schedule = relationship("TreatmentSchedule", back_populates="recovery_scans")

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    location_name = Column(String(255), nullable=False)
    temperature_c = Column(Float, nullable=False)
    humidity_percent = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=False)
    wind_speed_kmh = Column(Float, nullable=False)
    forecast_text = Column(String(255), nullable=False)
    warning = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, default="default-user-id")
    location_name = Column(String(255), nullable=False)
    crop_name = Column(String(255), nullable=False)
    disease_pest_name = Column(String(255), nullable=False)
    risk_level = Column(String(50), nullable=False)
    reason = Column(Text, nullable=False)
    preventive_action = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ExpertRequest(Base):
    __tablename__ = "expert_requests"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    farmer_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    crop_name = Column(String(255), nullable=False)
    image_url = Column(Text, nullable=True)
    question = Column(Text, nullable=False)
    status = Column(String(50), default="Open")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    farmer = relationship("User", back_populates="expert_requests")
    answers = relationship("ExpertAnswer", back_populates="request")

class ExpertAnswer(Base):
    __tablename__ = "expert_answers"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    request_id = Column(String(36), ForeignKey("expert_requests.id"), nullable=False)
    expert_name = Column(String(255), nullable=False)
    response_text = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    request = relationship("ExpertRequest", back_populates="answers")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    title = Column(String(255), default="Crop Consultation")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("chat_sessions.id"), nullable=False)
    sender = Column(String(50), nullable=False)
    text = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    voice_url = Column(Text, nullable=True)
    citations = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    session = relationship("ChatSession", back_populates="messages")

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class FertilizerCalculation(Base):
    __tablename__ = "fertilizer_calculations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    crop_name = Column(String(255), nullable=False)
    area_acres = Column(Float, nullable=False)
    nitrogen_req_kg = Column(Float, nullable=False)
    phosphorus_req_kg = Column(Float, nullable=False)
    potassium_req_kg = Column(Float, nullable=False)
    formula_explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
