# ruko_pipeline.py - audio -> transcript -> scam check -> spoken warning
import sys
from gnani_client import transcribe, speak
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

MESSAGES = {
    "HIGH": "रुकिए! यह एक जाने-पहचाने धोखाधड़ी के कॉल जैसा लगता है। "
            "पुलिस कभी वीडियो कॉल पर गिरफ्तार नहीं करती। पैसे मत भेजिए। "
            "कॉल काटिए और अपने परिवार को बताइए। पैसे चले गए हों तो तुरंत 1930 पर कॉल कीजिए।",
    "MEDIUM": "सावधान रहिए। इसमें धोखाधड़ी के कुछ संकेत दिख रहे हैं। "
              "ओटीपी या पैसे किसी को मत दीजिए। पहले अपने परिवार से पूछिए।",
    "LOW": "थोड़ा सावधान रहिए। अगर कोई पैसे या गुप्त रखने को कहे, तो रुकिए और परिवार से पूछिए।",
    "NONE": "मुझे कोई जाना-पहचाना धोखाधड़ी का संकेत नहीं मिला। "
            "लेकिन अगर कोई पैसे मांगे या किसी को बताने से मना करे, तो रुकिए और 1930 पर पूछिए।",
}


def run(audio_path):
    print("1. Listening...")
    text = transcribe(audio_path)
    print("   Heard:", text)

    print("2. Checking...")
    result = check(text)
    print("   Level:", result["level"], "| Score:", result["score"])
    print("   Signals:", list(result["signals"].keys()))

    print("3. Speaking warning...")
    out = speak(MESSAGES[result["level"]], out_path="warning.wav")
    print("   Saved:", out)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "test_scam.wav"
    run(path)