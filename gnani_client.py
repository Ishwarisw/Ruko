# gnani_client.py - talk to Gnani STT and TTS
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GNANI_API_KEY")

STT_URL = "https://api.vachana.ai/stt/v3"
TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"


def transcribe_bytes(audio_bytes, filename="audio.wav", language_code="hi-IN"):
    """Audio bytes -> text."""
    r = requests.post(
        STT_URL,
        headers={"X-API-Key-ID": API_KEY},
        files={"audio_file": (filename, audio_bytes)},
        data={"language_code": language_code},
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["transcript"]


def transcribe(audio_path, language_code="hi-IN"):
    """Audio file -> text."""
    with open(audio_path, "rb") as f:
        return transcribe_bytes(f.read(), os.path.basename(audio_path), language_code)


def speak_bytes(text, language="hi-IN", voice="Nalini"):
    """Text -> audio bytes (WAV)."""
    payload = {
        "text": text,
        "voice": voice,
        "model": "timbre-v2.5",
        "language": language,
        "speed": 0.9,
        "audio_config": {
            "sample_rate": 24000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav",
        },
    }
    r = requests.post(
        TTS_URL,
        headers={"Content-Type": "application/json", "X-API-Key-ID": API_KEY},
        json=payload,
        timeout=60,
    )
    r.raise_for_status()
    return r.content


def speak(text, out_path="reply.wav", language="hi-IN", voice="Nalini"):
    """Text -> audio file."""
    with open(out_path, "wb") as f:
        f.write(speak_bytes(text, language, voice))
    return out_path