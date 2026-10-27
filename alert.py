# alert.py - sends a Telegram message to a family contact. Demo only.
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_family_alert(level, heard_text, lang="hi-IN"):
    """Returns (ok, message). Only call this after the user presses the button."""
    if not TOKEN or not CHAT_ID:
        return False, "Telegram is not set up in .env"

    if lang == "mr-IN":
        text = (f"🛑 Ruko सूचना: एका कॉलमध्ये फसवणुकीची चिन्हे दिसली (धोका: {level}).\n"
                f"ऐकलेले: {heard_text}\n"
                "कृपया लगेच त्यांना फोन करा. पैसे पाठवू देऊ नका. गरज पडल्यास 1930 वर कॉल करा.")
    else:
        text = (f"🛑 Ruko अलर्ट: एक कॉल में धोखाधड़ी के संकेत मिले (खतरा: {level}).\n"
                f"सुना गया: {heard_text}\n"
                "कृपया तुरंत उन्हें फोन करें। पैसे मत भेजने दें। ज़रूरत हो तो 1930 पर कॉल करें।")

    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=15,
        )
        if r.status_code == 200:
            return True, "Family alert sent."
        return False, f"Telegram error {r.status_code}"
    except Exception as e:
        return False, f"Could not send: {e}"