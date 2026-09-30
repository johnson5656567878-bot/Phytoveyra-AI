"""
PlantVillage 38-Class Mapping and Helper Definitions.
Class index (0 to 37) matches the trained model class output order exactly.
"""

from typing import List, Dict, Any, Tuple

CLASS_NAMES: List[str] = [
    "Apple___Apple_scab",                           # 0
    "Apple___Black_rot",                            # 1
    "Apple___Cedar_apple_rust",                     # 2
    "Apple___healthy",                              # 3
    "Blueberry___healthy",                          # 4
    "Cherry___Powdery_mildew",                      # 5
    "Cherry___healthy",                             # 6
    "Corn___Cercospora_leaf_spot_Gray_leaf_spot",   # 7
    "Corn___Common_rust",                           # 8
    "Corn___Northern_Leaf_Blight",                  # 9
    "Corn___healthy",                               # 10
    "Grape___Black_rot",                            # 11
    "Grape___Esca_Black_Measles",                   # 12
    "Grape___Leaf_blight_Isariopsis_Leaf_Spot",     # 13
    "Grape___healthy",                              # 14
    "Orange___Haunglongbing_Citrus_greening",       # 15
    "Peach___Bacterial_spot",                       # 16
    "Peach___healthy",                              # 17
    "Pepper_bell___Bacterial_spot",                 # 18
    "Pepper_bell___healthy",                        # 19
    "Potato___Early_blight",                        # 20
    "Potato___Late_blight",                         # 21
    "Potato___healthy",                             # 22
    "Raspberry___healthy",                          # 23
    "Soybean___healthy",                            # 24
    "Squash___Powdery_mildew",                      # 25
    "Strawberry___Leaf_scorch",                     # 26
    "Strawberry___healthy",                         # 27
    "Tomato___Bacterial_spot",                      # 28
    "Tomato___Early_blight",                        # 29
    "Tomato___Late_blight",                         # 30
    "Tomato___Leaf_Mold",                           # 31
    "Tomato___Septoria_leaf_spot",                  # 32
    "Tomato___Spider_mites_Two-spotted_spider_mite",# 33
    "Tomato___Target_Spot",                         # 34
    "Tomato___Tomato_mosaic_virus",                 # 35
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",       # 36
    "Tomato___healthy"                              # 37
]

HEALTHY_CLASS_NAMES: List[str] = [
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry___healthy",
    "Corn___healthy",
    "Grape___healthy",
    "Peach___healthy",
    "Pepper_bell___healthy",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Strawberry___healthy",
    "Tomato___healthy"
]

CROP_DISPLAY_MAP: Dict[str, str] = {
    "Apple": "Apple",
    "Blueberry": "Blueberry",
    "Cherry": "Cherry",
    "Corn": "Corn / Maize",
    "Grape": "Grape",
    "Orange": "Orange / Citrus",
    "Peach": "Peach",
    "Pepper_bell": "Bell Pepper",
    "Potato": "Potato",
    "Raspberry": "Raspberry",
    "Soybean": "Soybean",
    "Squash": "Squash",
    "Strawberry": "Strawberry",
    "Tomato": "Tomato"
}

def parse_class_info(class_name: str) -> Dict[str, Any]:
    """
    Parses a PlantVillage class string into structured crop name, condition, and condition_type.
    """
    if "___" not in class_name:
        return {
            "crop": "Unknown",
            "condition": class_name,
            "condition_type": "unknown",
            "is_healthy": False
        }

    raw_crop, raw_condition = class_name.split("___", 1)
    crop_display = CROP_DISPLAY_MAP.get(raw_crop, raw_crop.replace("_", " "))

    if raw_condition.lower() == "healthy":
        return {
            "crop": crop_display,
            "condition": "Healthy",
            "condition_type": "healthy",
            "is_healthy": True
        }

    # Format human-readable condition title
    formatted_condition = raw_condition.replace("_", " ")
    
    # Specific condition type classification
    condition_type = "disease"
    if "spider_mite" in raw_condition.lower() or "pest" in raw_condition.lower():
        condition_type = "pest"
    elif "virus" in raw_condition.lower():
        condition_type = "disease"

    return {
        "crop": crop_display,
        "condition": formatted_condition,
        "condition_type": condition_type,
        "is_healthy": False
    }
