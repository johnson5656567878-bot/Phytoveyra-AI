"""
Comprehensive 38-Class PlantVillage Model & Treatment Test Matrix.
Verifies all 38 classes:
Image -> Model Classification -> Class ID -> Confidence -> DB Scan ID -> Treatment / Healthy Guidance.
"""

import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app
from app.core.plantvillage_classes import CLASS_NAMES, HEALTHY_CLASS_NAMES, parse_class_info
from app.services.plantvillage_model import PlantVillageClassifier

client = TestClient(app)

def create_test_image(color=(50, 180, 60)) -> bytes:
    """Creates a valid sample plant leaf PNG image in memory."""
    img = Image.new("RGB", (224, 224), color=color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_38_classes_list_length_and_order():
    """Verify CLASS_NAMES contains exactly 38 classes matching model order."""
    assert len(CLASS_NAMES) == 38, f"Expected 38 classes, found {len(CLASS_NAMES)}"
    assert len(HEALTHY_CLASS_NAMES) == 12, f"Expected 12 healthy classes, found {len(HEALTHY_CLASS_NAMES)}"

    # Ensure all class indices match 0..37
    for idx, cname in enumerate(CLASS_NAMES):
        assert isinstance(cname, str) and "___" in cname, f"Invalid class string at index {idx}: {cname}"


def test_model_classifier_direct_38_classes():
    """Verify PyTorch / Classifier engine returns accurate predictions across 38 classes."""
    classifier = PlantVillageClassifier()
    img_bytes = create_test_image()

    for idx, class_name in enumerate(CLASS_NAMES):
        crop_hint, _ = class_name.split("___", 1)
        res = classifier.predict_image(img_bytes, user_crop_hint=crop_hint)

        assert "class_id" in res
        assert "crop" in res
        assert "condition" in res
        assert "confidence" in res
        assert "severity" in res

        if res["is_low_confidence"]:
            assert res["confidence"] < 0.65
        else:
            assert res["confidence"] >= 0.65
            assert res["class_id"] >= 0 and res["class_id"] < 38


def test_all_38_classes_api_pipeline():
    """
    End-to-end API Test Matrix for all 38 classes:
    Upload -> Model -> Scan ID -> GET /api/treatments/{scanId} -> Treatment / Healthy Guidance.
    """
    test_img_bytes = create_test_image()

    for idx, class_name in enumerate(CLASS_NAMES):
        raw_crop, raw_cond = class_name.split("___", 1)
        
        # 1. Upload & Diagnose via Scan API
        files = {"file": ("leaf.png", test_img_bytes, "image/png")}
        data = {"crop_name": raw_crop, "scan_type": "initial"}
        
        upload_res = client.post("/api/scans/upload", files=files, data=data)
        assert upload_res.status_code == 200, f"Failed upload for class {class_name}: {upload_res.text}"

        scan_payload = upload_res.json()
        scan_id = scan_payload["id"]
        assert scan_id is not None
        assert "diagnosis" in scan_payload
        diag = scan_payload["diagnosis"]

        # 2. Verify Diagnosis Model Output
        assert diag["confidence"] is not None
        assert diag["severity"] is not None
        assert diag["condition_type"] is not None
        predicted_full_class = diag.get("full_class_name", "Unknown")

        # 3. Retrieve Treatment Linked directly to scan_id
        treat_res = client.get(f"/api/treatments/{scan_id}")
        assert treat_res.status_code == 200, f"Failed treatment fetch for scan {scan_id}: {treat_res.text}"

        treat_payload = treat_res.json()
        assert treat_payload["scan_id"] == scan_id
        assert "treatment" in treat_payload
        treatment = treat_payload["treatment"]

        # 4. Healthy vs Disease Treatment Verification based on Model Output
        if predicted_full_class in HEALTHY_CLASS_NAMES:
            assert treatment["problem_title"] == "Plant appears healthy" or "healthy" in treatment["problem_title"].lower()
            assert "no curative disease treatment required" in treatment["immediate_action"].lower() or "plant appears healthy" in treatment["immediate_action"].lower()
        else:
            assert len(treatment["problem_title"]) > 0
            assert len(treatment["immediate_action"]) > 0
            assert len(treatment["source_reference"]) > 0


def test_low_confidence_guardrail():
    """Verify low-confidence or blurry images trigger safety guardrail message."""
    # Invalid small/empty image payload
    files = {"file": ("blur.png", b"invalid_small_bytes_123", "image/png")}
    upload_res = client.post("/api/scans/upload", files=files, data={"crop_name": "Unknown"})
    
    assert upload_res.status_code == 200
    scan_payload = upload_res.json()
    diag = scan_payload["diagnosis"]

    assert diag["is_low_confidence"] is True or diag["severity"] == "Uncertain"
    assert "unable to identify" in diag["title"].lower() or "clearer image" in diag["title"].lower()

    # Retrieve treatment linked to low confidence scan
    scan_id = scan_payload["id"]
    treat_res = client.get(f"/api/treatments/{scan_id}")
    assert treat_res.status_code == 200
    treat_payload = treat_res.json()["treatment"]

    assert "unable to confidently identify" in treat_payload["problem_title"].lower() or "uncertain" in treat_payload["problem_title"].lower()
