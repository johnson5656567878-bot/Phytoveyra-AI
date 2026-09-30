"""
API Router for AI Farmer Chatbot & RAG Integration.
Provides /api/chat (POST) and /api/chat/query (POST) endpoints connected to the LLM / RAG service.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter
from app.schemas.schemas import ChatMessageCreate, ChatMessageResponse
from app.services.rag_service import RAGService
from app.services.voice_service import VoiceService

chat_router = APIRouter(prefix="/chat", tags=["AI Farmer Chatbot & RAG"])
voice_router = APIRouter(prefix="/voice", tags=["Voice Assistant STT/TTS"])


def _build_chat_response(msg: ChatMessageCreate) -> ChatMessageResponse:
    """Core chat logic — sends user message to RAG/LLM and returns response."""
    rag_res = RAGService.query(
        user_question=msg.text,
        language=msg.language or "en",
        history=msg.history,
        context_farmer_data=None
    )

    return {
        "id": f"msg-resp-{uuid.uuid4().hex[:8]}",
        "session_id": msg.session_id or f"sess-{uuid.uuid4().hex[:8]}",
        "sender": "assistant",
        "text": rag_res["answer"],
        "image_url": None,
        "citations": rag_res.get("citations", []),
        "created_at": datetime.now(timezone.utc)
    }


@chat_router.post("", response_model=ChatMessageResponse, summary="Send a chat message")
async def chat_endpoint(msg: ChatMessageCreate):
    """Primary chat endpoint — POST /api/chat"""
    return _build_chat_response(msg)


@chat_router.post("/query", response_model=ChatMessageResponse, summary="Send a chat query (alias)")
async def chat_query_endpoint(msg: ChatMessageCreate):
    """Alias chat endpoint — POST /api/chat/query"""
    return _build_chat_response(msg)


@voice_router.post("/stt")
async def speech_to_text(audio_payload: Dict[str, Any]):
    audio_b64 = audio_payload.get("audio_base64", "")
    lang = audio_payload.get("language", "en")
    return VoiceService.process_speech_to_text(audio_b64, lang)


@voice_router.post("/tts")
async def text_to_speech(tts_payload: Dict[str, Any]):
    text = tts_payload.get("text", "")
    lang = tts_payload.get("language", "en")
    return VoiceService.process_text_to_speech(text, lang)
