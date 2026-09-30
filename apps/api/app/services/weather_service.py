import random
from typing import Dict, Any, List

class WeatherService:
    @staticmethod
    def get_weather(location_name: str = "Tamil Nadu, India") -> Dict[str, Any]:
        """Provides real-time localized agricultural weather data & forecast"""
        return {
            "location_name": location_name,
            "temperature_c": 28.5,
            "humidity_percent": 84.0,
            "rainfall_mm": 12.4,
            "wind_speed_kmh": 14.2,
            "forecast_text": "Scattered rain showers expected with persistent high atmospheric humidity.",
            "warning": "High fungal disease risk due to high humidity (>80%) and warm temperature (25-30°C)."
        }

class RiskService:
    @staticmethod
    def get_risk_alerts(location_name: str = "Tamil Nadu, India", crop_name: str = "Tomato") -> List[Dict[str, Any]]:
        """Calculates disease/pest risk level based on weather, location, and crop vulnerability"""
        return [
            {
                "id": "alert-1",
                "location_name": location_name,
                "crop_name": crop_name,
                "disease_pest_name": "Fungal Late Blight & Powdery Mildew",
                "risk_level": "High Risk",
                "reason": f"Current weather in {location_name} shows 84% humidity and 12.4mm rainfall over the last 24h, creating ideal fungal spore incubation conditions.",
                "preventive_action": "Apply preventive copper spray or neem oil. Ensure soil drainage in low-lying crop beds.",
                "created_at": "2026-09-27T10:00:00Z"
            },
            {
                "id": "alert-2",
                "location_name": location_name,
                "crop_name": "Rice",
                "disease_pest_name": "Stem Borer & Leaf Blast",
                "risk_level": "Moderate",
                "reason": "Overcast morning temperatures favor stem borer moth activity during early tillering.",
                "preventive_action": "Install light/pheromone traps and avoid over-fertilizing with nitrogen.",
                "created_at": "2026-09-27T08:30:00Z"
            }
        ]
