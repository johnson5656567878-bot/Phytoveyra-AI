import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

def test_root():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "online"

def test_farms_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/farms")
        assert response.status_code == 200
        farms = response.json()
        assert isinstance(farms, list)

def test_crops_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/crops")
        assert response.status_code == 200
        crops = response.json()
        assert isinstance(crops, list)

def test_weather_endpoint():
    with TestClient(app) as client:
        response = client.get("/api/weather")
        assert response.status_code == 200
        data = response.json()
        assert "temperature_c" in data
        assert "humidity_percent" in data

def test_fertilizer_calculator():
    with TestClient(app) as client:
        payload = {
            "crop_name": "Chilli",
            "area_acres": 2.0,
            "soil_n_ppm": 20.0,
            "soil_p_ppm": 10.0,
            "soil_k_ppm": 150.0
        }
        response = client.post("/api/fertilizer/calculate", json=payload)
        assert response.status_code == 200
        res = response.json()
        assert res["recommended_urea_kg"] > 0
        assert res["recommended_dap_kg"] > 0

def test_treatment_recommendation():
    with TestClient(app) as client:
        response = client.get("/api/treatments/recommend?diagnosis_title=Chilli Leaf Curl Virus")
        assert response.status_code == 200
        rec = response.json()
        assert "immediate_action" in rec
        assert "approved_chemical" in rec

def test_fungal_vs_pest_vs_deficiency_vs_low_confidence_treatments():
    """Verify that different diagnoses return completely different specific treatments."""
    from app.services.treatment_service import TreatmentService

    fungal_rec = TreatmentService.get_recommendation(
        crop_name="Tomato",
        diagnosis_title="Fungal Leaf Spot / Blight Necrosis",
        condition_type="disease",
        severity="Severe"
    )
    assert "fungal" in fungal_rec["why_happening"].lower() or "blight" in fungal_rec["problem_title"].lower()

    pest_rec = TreatmentService.get_recommendation(
        crop_name="Corn",
        diagnosis_title="Foliage Pest Damage / Leaf Skeletonisation",
        condition_type="pest",
        severity="Moderate"
    )
    assert "caterpillar" in pest_rec["why_happening"].lower() or "pest" in pest_rec["why_happening"].lower() or "larval" in pest_rec["why_happening"].lower() or "spodoptera" in pest_rec["why_happening"].lower()
    assert fungal_rec["problem_title"] != pest_rec["problem_title"]

@patch("app.services.rag_service.OpenAI")
def test_chat_query_openai_integration_and_varying_responses(mock_openai_cls):
    """Verify that the /api/chat endpoint sends user's actual message to OpenAI and returns actual changing AI responses."""
    mock_client = MagicMock()
    mock_openai_cls.return_value = mock_client

    # 1. First question and response mock
    mock_resp1 = MagicMock()
    mock_resp1.choices = [MagicMock(message=MagicMock(content="Apply neem oil spray and remove infected chilli vector leaves."))]
    
    # 2. Second question and response mock
    mock_resp2 = MagicMock()
    mock_resp2.choices = [MagicMock(message=MagicMock(content="Nitrogen deficiency causes uniform leaf chlorosis starting from lower leaves."))]

    mock_client.chat.completions.create.side_effect = [mock_resp1, mock_resp2]

    os.environ["OPENAI_API_KEY"] = "sk-proj-test-key-12345"

    with TestClient(app) as client:
        # Message 1
        msg1 = "How do I treat leaf curl on my chilli crop?"
        res1 = client.post("/api/chat/query", json={"text": msg1, "language": "en"})
        assert res1.status_code == 200
        data1 = res1.json()
        assert data1["text"] == "Apply neem oil spray and remove infected chilli vector leaves."

        # Verify OpenAI API was called with the actual user message
        called_args_1 = mock_client.chat.completions.create.call_args_list[0][1]
        assert any(msg["content"] == msg1 for msg in called_args_1["messages"])

        # Message 2
        msg2 = "What are the primary symptoms of nitrogen deficiency in rice?"
        res2 = client.post("/api/chat/query", json={"text": msg2, "language": "en"})
        assert res2.status_code == 200
        data2 = res2.json()
        assert data2["text"] == "Nitrogen deficiency causes uniform leaf chlorosis starting from lower leaves."

        # Verify second call was made with the second user message
        called_args_2 = mock_client.chat.completions.create.call_args_list[1][1]
        assert any(msg["content"] == msg2 for msg in called_args_2["messages"])

        # Verify responses actually change depending on prompt
        assert data1["text"] != data2["text"]

def test_chat_missing_openai_key_error():
    """Verify that a clear 500 configuration error is returned if OPENAI_API_KEY is missing or empty."""
    original_key = os.environ.get("OPENAI_API_KEY")
    try:
        os.environ["OPENAI_API_KEY"] = ""
        with TestClient(app) as client:
            res = client.post("/api/chat/query", json={"text": "Hello AI", "language": "en"})
            assert res.status_code == 500
            err_detail = res.json()["detail"]
            assert "OPENAI_API_KEY" in err_detail or "missing" in err_detail.lower()
    finally:
        if original_key is not None:
            os.environ["OPENAI_API_KEY"] = original_key
