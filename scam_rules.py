# scam_rules.py - simple scam-pattern detector (Hindi / Marathi / Hinglish / English)
import unicodedata

SIGNALS = {
    "authority_claim": {
        "weight": 2,
        "words": ["cbi", "सीबीआई", "सी बी आई", "police", "पुलिस", "पोलीस",
                  "enforcement directorate", "प्रवर्तन निदेशालय", "customs",
                  "कस्टम", "narcotics", "नारकोटिक्स", "trai", "ट्राई",
                  "cyber crime", "साइबर क्राइम", "सायबर", "rbi", "आरबीआई",
                  "आर बी आई", "court", "कोर्ट", "न्यायालय", "अधिकारी"],
    },
    "digital_arrest": {
        "weight": 4,
        "words": ["digital arrest", "डिजिटल अरेस्ट", "डिजिटल अटक",
                  "डिजिटल अटकेत", "गिरफ्तार", "अटक", "arrest warrant", "वारंट",
                  "मनी लॉन्ड्रिंग", "मनी लॉन्डरिंग", "money laundering"],
    },
    "secrecy": {
        "weight": 4,
        "words": ["किसी को मत बताइए", "किसी को न बताएं", "किसी को मत बताना",
                  "कोणाला सांगू नका", "कुणाला सांगू नका", "don't tell anyone",
                  "do not tell anyone", "घरवालों को मत", "परिवार को मत",
                  "कॉल कट मत", "फोन मत काटिए", "कॉल कट करू नका"],
    },
    "money_demand": {
        "weight": 3,
        "words": ["पैसे ट्रांसफर", "पैसा ट्रांसफर", "पैसे भेज", "पैसा भेज",
                  "पैसे पाठवा", "पैसे पाठव", "ट्रांसफर करो", "ट्रांसफर कर",
                  "transfer", "जमा करना", "verification के लिए", "सत्यापन",
                  "सुरक्षित खाते", "safe account", "आरबीआई खाते"],
    },
    "urgency": {
        "weight": 2,
        "words": ["अभी", "तुरंत", "लगेच", "आत्ताच", "immediately", "right now",
                  "आज ही", "एक घंटे", "30 मिनट"],
    },
    "sensitive_info": {
        "weight": 3,
        "words": ["otp", "ओटीपी", "ओ टी पी", "पिन नंबर", "pin number", "cvv",
                  "आधार नंबर", "aadhaar", "पासवर्ड", "password", "anydesk",
                  "teamviewer"],
    },
}


def normalize(text):
    """Lowercase, and remove the nukta dot so ट्रांसफ़र and ट्रांसफर match."""
    t = unicodedata.normalize("NFD", text.lower())
    t = t.replace("\u093c", "")
    return unicodedata.normalize("NFC", t)


def check(text):
    t = normalize(text)
    t_nospace = t.replace(" ", "")
    found = {}
    score = 0
    for name, info in SIGNALS.items():
        hits = []
        for w in info["words"]:
            w = normalize(w)
            if w in t or (" " in w and w.replace(" ", "") in t_nospace):
                hits.append(w)
        if hits:
            found[name] = hits
            score += info["weight"]

    if score >= 7:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    elif score >= 2:
        level = "LOW"
    else:
        level = "NONE"
    return {"level": level, "score": score, "signals": found}


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    tests = [
        "मैं पुलिस बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसा ट्रांसफ़र करो।",
        "मी पोलीस बोलतोय, तुम्ही डिजिटल अटकेत आहात, कोणाला सांगू नका आणि आत्ताच पैसे पाठवा.",
        "आपका बैंक OTP शेयर कीजिए तुरंत",
        "नमस्ते, आपका कूरियर कल सुबह 10:00 बजे पहुँच जाएगा।",
        "I called you while shopping, I need a ride",
    ]
    for t in tests:
        print(t)
        print("  ->", check(t))