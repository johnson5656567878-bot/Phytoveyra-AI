export interface User {
  id: string;
  email: string;
  full_name: string;
  role_name: 'Farmer' | 'Expert' | 'Admin';
  preferred_language: string;
  phone_number?: string;
  location_name?: string;
  latitude?: number;
  longitude?: number;
}

export interface Farm {
  id: string;
  user_id: string;
  name: string;
  location: string;
  latitude?: number;
  longitude?: number;
  total_area_acres: number;
  soil_type: string;
  irrigation_type: string;
}

export interface Crop {
  id: string;
  farm_id?: string;
  name: string;
  variety?: string;
  planting_date?: string;
  area_acres: number;
  growth_stage: string;
  health_status: 'Healthy' | 'Warning' | 'High Risk' | 'Critical';
  created_at: string;
}

export interface Diagnosis {
  id: string;
  scan_id: string;
  condition_type: 'disease' | 'pest' | 'nutrient_deficiency' | 'healthy' | 'unknown';
  title: string;
  confidence: number;
  severity: 'Mild' | 'Moderate' | 'Severe' | 'Critical' | 'Healthy' | 'Uncertain';
  symptoms: string[];
  causes: string[];
  heatmap_url?: string;
  explanation_reasoning?: string;
  is_low_confidence: boolean;
  recommended_next_step?: string;
}

export interface PlantScan {
  id: string;
  user_id: string;
  crop_id?: string;
  crop_name?: string;
  image_url: string;
  notes?: string;
  scan_type: 'initial' | 'follow_up';
  created_at: string;
  diagnosis?: Diagnosis;
}

export interface TreatmentRecommendation {
  id: string;
  diagnosis_id: string;
  problem_title: string;
  why_happening: string;
  immediate_action: string;
  cultural_control?: string;
  biological_organic?: string;
  approved_chemical?: string;
  safety_warning?: string;
  follow_up_days: number;
  source_reference: string;
}

export interface TreatmentSchedule {
  id: string;
  crop_id?: string;
  scan_id?: string;
  treatment_id?: string;
  action_item: string;
  scheduled_date: string;
  follow_up_date: string;
  status: 'Pending' | 'Completed' | 'Rescheduled' | 'Cancelled';
  notes?: string;
}

export interface RecoveryScan {
  id: string;
  schedule_id?: string;
  original_scan_id: string;
  followup_image_url: string;
  initial_severity: string;
  current_severity: string;
  improvement_percentage?: number;
  recovery_status: 'Improving' | 'Stable' | 'Worsening' | 'Uncertain';
  analysis_notes?: string;
  initial_image_url: string;
}

export interface WeatherData {
  location_name: string;
  temperature_c: number;
  humidity_percent: number;
  rainfall_mm: number;
  wind_speed_kmh: number;
  forecast_text: string;
  warning?: string;
}

export interface RiskAlert {
  id: string;
  location_name: string;
  crop_name: string;
  disease_pest_name: string;
  risk_level: 'Low' | 'Moderate' | 'High Risk' | 'Critical';
  reason: string;
  preventive_action: string;
  created_at: string;
}
