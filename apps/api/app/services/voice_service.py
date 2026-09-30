import base64
from typing import Dict, Any

class VoiceService:
    @staticmethod
    def process_speech_to_text(audio_base64: str, language: str = "en") -> Dict[str, Any]:
        """
        Processes audio input into recognized text.
        Supports Tamil, English, Hindi, Telugu, Malayalam, Kannada.
        """
        # Simulated STT recognition
        sample_transcripts = {
            "en": "What disease is affecting my tomato plant leaf?",
            "ta": "என் தக்காளிச் செடியில் என்ன நோய் பாதித்துள்ளது?",
            "hi": "मेरे टमाटर के पौधे में कौन सी बीमारी है?",
            "te": "నా టమాటా మొక్కకి ఏ వ్యాధి సోకింది?",
            "ml": "എന്റെ തക്കാളി ചെടിയെ ബാധിച്ച രോഗം ഏതാണ്?",
            "kn": "ನನ್ನ ಟೊಮೆಟೊ ಗಿಡಕ್ಕೆ ಯಾವ ರೋಗ ಬಂದಿದೆ?"
        }
        text = sample_transcripts.get(language, sample_transcripts["en"])
        return {
            "recognized_text": text,
            "detected_language": language,
            "confidence": 0.95
        }

    @staticmethod
    def process_text_to_speech(text: str, language: str = "en") -> Dict[str, Any]:
        """
        Synthesizes text into audio playback payload.
        """
        return {
            "text": text,
            "language": language,
            "audio_format": "mp3",
            "audio_url": None, # Web Speech API synthesized on browser side
            "status": "ready"
        }
