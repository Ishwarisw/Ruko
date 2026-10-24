import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GNANI_API_KEY")

url = "https://api.vachana.ai/stt/v3"
headers = {"X-API-Key-ID": API_KEY}

with open("reply.wav", "rb") as f:
    files = {"audio_file": f}
    data = {"language_code": "hi-IN"}
    response = requests.post(url, headers=headers, files=files, data=data)

print("Status:", response.status_code)
print(response.text)