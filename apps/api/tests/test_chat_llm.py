"""
Automated Test Suite for PhytoVeyra AI Assistant LLM & Chat Endpoints.
Verifies multi-turn history and unique responses for test questions:
1. "Hi"
2. "Hello"
3. "What is plant disease?"
4. "What is tomato yellow leaf curl virus?"
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint_questions():
    test_questions = [
        "Hi",
        "Hello",
        "What is plant disease?",
        "What is tomato yellow leaf curl virus?"
    ]

    responses = []
    history = []

    for q in test_questions:
        payload = {
            "text": q,
            "language": "en",
            "session_id": "test-session-101",
            "history": history
        }

        res = client.post("/api/chat", json=payload)
        assert res.status_code == 200, f"Chat API error for query '{q}': {res.text}"
        
        data = res.json()
        assert "text" in data
        assert "citations" in data
        assert len(data["text"]) > 10, f"Response too short for query '{q}'"

        response_text = data["text"]
        responses.append(response_text)

        # Update history for multi-turn test
        history.append({"sender": "user", "text": q})
        history.append({"sender": "assistant", "text": response_text})

    # Verify that responses are distinct and non-duplicate
    assert len(set(responses)) == 4, "Expected 4 distinct AI responses for different queries."

    # Specific topic checks
    assert "greetings" in responses[0].lower() or "hello" in responses[0].lower() or "assist" in responses[0].lower()
    assert "abnormality" in responses[2].lower() or "fungal" in responses[2].lower() or "pathogen" in responses[2].lower() or "disease" in responses[2].lower()
    assert "begomovirus" in responses[3].lower() or "whitefly" in responses[3].lower() or "curling" in responses[3].lower() or "tylcv" in responses[3].lower()


def test_chat_query_legacy_endpoint():
    payload = {
        "text": "What is plant disease?",
        "language": "en"
    }
    res = client.post("/api/chat/query", json=payload)
    assert res.status_code == 200
    assert "text" in res.json()
