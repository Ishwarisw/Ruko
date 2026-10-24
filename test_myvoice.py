import sys
import requests
from gnani_client import API_KEY, STT_URL
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

path = sys.argv[1] if len(sys.argv) > 1 else "mytest.ogg"
lang = sys.argv[2] if len(sys.argv) > 2 else "hi-IN"

with open(path, "rb") as f:
    r = requests.post(
        STT_URL,
        headers={"X-API-Key-ID": API_KEY},
        files={"audio_file": (path, f)},
        data={"language_code": lang},
        timeout=60,
    )

print("Status:", r.status_code)
print(r.text)

if r.status_code == 200:
    text = r.json()["transcript"]
    print("\nHeard:", text)
    print("Result:", check(text))