# make_test_audio.py - makes fake test calls (synthetic, no real data)
import sys
from gnani_client import speak

sys.stdout.reconfigure(encoding="utf-8")

SCAM = "मैं CBI से बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसे ट्रांसफर करो"
NORMAL = "नमस्ते, आपका कूरियर कल सुबह दस बजे पहुँच जाएगा"

speak(SCAM, out_path="test_scam.wav", voice="Deepak")
print("Made test_scam.wav")
speak(NORMAL, out_path="test_normal.wav", voice="Deepak")
print("Made test_normal.wav")