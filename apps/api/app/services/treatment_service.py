"""
Treatment Service linking plant scan diagnosis to grounded 38-class knowledge base.
Ensures healthy classes receive "Plant appears healthy" with preventive guidance.
Ensures low-confidence scans receive "Unable to confidently identify this condition."
"""

from typing import Dict, Any, Optional
from app.services.treatment_knowledge_38 import get_treatment_for_class, TREATMENT_KNOWLEDGE_38
from app.core.plantvillage_classes import HEALTHY_CLASS_NAMES, parse_class_info

class TreatmentService:
    @staticmethod
    def get_recommendation(
        full_class_name: str = "Unknown",
        crop_name: str = "Unknown",
        diagnosis_title: str = "",
        condition_type: str = "unknown",
        severity: str = "Moderate",
        is_low_confidence: bool = False,
        confidence: float = 0.85
    ) -> Dict[str, Any]:

        # 1. Low Confidence / Guardrail check (< 0.65 or is_low_confidence is true)
        if is_low_confidence or confidence < 0.65 or condition_type == "unknown" or "unable to identify" in diagnosis_title.lower():
            return {
                "problem_title": "Unable to confidently identify this condition.",
                "why_happening": "Exact plant condition could not be identified above the 65% confidence guardrail threshold.",
                "immediate_action": "No reliable diagnosis available, so a specific treatment cannot be recommended.",
                "cultural_control": "Inspect the crop physically, verify sunlight, soil moisture, and leaf symptoms under daylight.",
                "biological_organic": "No biological treatment recommendation available for uncertain diagnosis. Consult local agricultural extension professional.",
                "approved_chemical": "No chemical recommendation available for uncertain diagnosis. Consult local agricultural extension professional.",
                "safety_warning": "Do not apply chemical pesticides without confirmed diagnostic identification.",
                "follow_up_days": 3,
                "source_reference": "Agricultural Extension Safety Guardrail Protocol"
            }

        # 2. Healthy Class Check
        if full_class_name in HEALTHY_CLASS_NAMES or condition_type == "healthy" or "healthy" in diagnosis_title.lower():
            parsed = parse_class_info(full_class_name) if full_class_name in HEALTHY_CLASS_NAMES else {"crop": crop_name or "Plant"}
            crop_display = parsed.get("crop", crop_name or "Plant")
            
            # Fetch grounded healthy preventive entry from 38-class knowledge base
            healthy_entry = get_treatment_for_class(full_class_name) if full_class_name in HEALTHY_CLASS_NAMES else None
            
            if healthy_entry:
                return healthy_entry

            return {
                "problem_title": "Plant appears healthy",
                "why_happening": f"The {crop_display.lower()} crop exhibits vibrant chlorophyll greening, normal leaf cell structure, and no visible pathogenic lesions or pest damage.",
                "immediate_action": "Plant appears healthy. No curative disease treatment required.",
                "cultural_control": f"Maintain regular irrigation and balanced organic soil fertility suitable for {crop_display.lower()}.",
                "biological_organic": "Apply organic compost mulching around root zone to nourish beneficial soil microbes.",
                "approved_chemical": "No chemical pesticide treatment needed for healthy crop foliage.",
                "safety_warning": "Avoid unnecessary chemical applications to preserve beneficial insects and soil micro-flora.",
                "follow_up_days": 14,
                "source_reference": "ICAR Good Agricultural Practices (GAP)"
            }

        # 3. Direct lookup in 38-Class Treatment Knowledge Base
        if full_class_name in TREATMENT_KNOWLEDGE_38:
            return dict(TREATMENT_KNOWLEDGE_38[full_class_name])

        # 4. Fallback lookup by matching title keywords
        title_lower = (diagnosis_title or "").lower()
        for cname, entry in TREATMENT_KNOWLEDGE_38.items():
            if cname in HEALTHY_CLASS_NAMES:
                continue
            raw_c, raw_cond = cname.split("___", 1)
            formatted_cond = raw_cond.replace("_", " ").lower()
            if formatted_cond in title_lower or raw_c.lower() in title_lower:
                return dict(entry)

        # Generic grounded treatment fallback
        display_crop = crop_name if crop_name not in ["Unknown", "Auto-Detect", ""] else "Crop"
        return {
            "problem_title": f"{display_crop} - {diagnosis_title}",
            "why_happening": f"Condition associated with {diagnosis_title} symptoms observed on {display_crop.lower()} foliage.",
            "immediate_action": f"Scout {display_crop.lower()} crop field for symptom spread and prune heavily affected leaves.",
            "cultural_control": f"Maintain proper field sanitation, plant spacing, and balanced irrigation for {display_crop.lower()}.",
            "biological_organic": "Apply biological Trichoderma viride or Neem extract foliar spray.",
            "approved_chemical": "Apply registered broad-spectrum protective fungicide/insecticide adhering strictly to label instructions.",
            "safety_warning": "Follow local pesticide safety regulations and wear protective mask and gloves.",
            "follow_up_days": 7,
            "source_reference": "Agricultural Extension Service Knowledge Base"
        }
