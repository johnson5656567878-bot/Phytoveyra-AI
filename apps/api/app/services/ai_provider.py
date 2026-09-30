"""
AI Vision Provider integrating the PyTorch 38-Class PlantVillage Model.
Analyzes uploaded plant photo bytes and returns model predictions matching 38 PlantVillage classes.
"""

from typing import Dict, Any
from app.services.plantvillage_model import PlantVillageClassifier

class AIProvider:
    async def analyze_image(self, image_bytes: bytes, crop_name: str = "Auto-Detect") -> Dict[str, Any]:
        raise NotImplementedError

class RealVisionAIProvider(AIProvider):
    def __init__(self):
        self.classifier = PlantVillageClassifier()

    async def analyze_image(self, image_bytes: bytes, crop_name: str = "Auto-Detect") -> Dict[str, Any]:
        # Perform 38-class model prediction
        pred = self.classifier.predict_image(image_bytes, user_crop_hint=crop_name)

        if pred["is_low_confidence"]:
            return {
                "class_id": -1,
                "full_class_name": "Unknown",
                "condition_type": "unknown",
                "title": "Unable to identify the plant problem confidently. Please upload a clearer image.",
                "confidence": pred["confidence"],
                "severity": "Uncertain",
                "symptoms": ["Uncertain image features detected"],
                "causes": ["The photo does not clearly match any of the 38 recognized crop condition profiles."],
                "heatmap_url": None,
                "explanation_reasoning": pred["recommended_next_step"],
                "is_low_confidence": True,
                "recommended_next_step": "Please upload a clearer close-up photo of plant foliage under clear daylight."
            }

        # Format title based on condition
        if pred["condition_type"] == "healthy":
            title = f"{pred['crop']} - Healthy Foliage"
            symptoms = [
                "Vibrant green leaf blade color with high chlorophyll density",
                "No significant necrotic spots or pest damage detected"
            ]
            causes = [
                "Balanced soil moisture and nutrient availability",
                "Adequate sunlight and canopy airflow"
            ]
        else:
            title = f"{pred['crop']} - {pred['condition']}"
            symptoms = [
                f"Characteristic {pred['condition'].lower()} lesions identified on {pred['crop']} foliage",
                "Foliar tissue discoloration and surface leaf damage"
            ]
            causes = [
                f"Pathogenic or environmental conditions promoting {pred['condition'].lower()}",
                "Elevated atmospheric humidity or vector transmission"
            ]

        return {
            "class_id": pred["class_id"],
            "full_class_name": pred["full_class_name"],
            "condition_type": pred["condition_type"],
            "title": title,
            "crop": pred["crop"],
            "condition": pred["condition"],
            "confidence": pred["confidence"],
            "severity": pred["severity"],
            "symptoms": symptoms,
            "causes": causes,
            "heatmap_url": pred["heatmap_url"],
            "explanation_reasoning": f"PyTorch 38-class model classified image as class ID {pred['class_id']} ({pred['full_class_name']}) with {round(pred['confidence']*100,1)}% confidence.",
            "is_low_confidence": False,
            "recommended_next_step": pred["recommended_next_step"]
        }
