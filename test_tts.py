import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GNANI_API_KEY")

url = "https://api.vachana.ai/api/v1/tts/inference"
headers = {
    "Content-Type": "application/json",
    "X-API-Key-ID": API_KEY,
}
payload = {
    "text": "यह एक धोखाधड़ी का कॉल हो सकता है। पैसे मत भेजिए।",
    "voice": "Nalini",
    "model": "timbre-v2.5",
    "language": "hi-IN",
    "speed": 0.9,
    "audio_config": {
        "sample_rate": 24000,
        "num_channels": 1,
        "sample_width": 2,
        "encoding": "linear_pcm",
        "container": "wav",
    },
}

response = requests.post(url, headers=headers, json=payload)
print("Status:", response.status_code)
print("Content-Type:", response.headers.get("Content-Type"))

if response.status_code == 200:
    with open("reply.wav", "wb") as f:
        f.write(response.content)
    print("Saved reply.wav -", len(response.content), "bytes")
else:
    print(response.text)