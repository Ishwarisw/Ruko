# scam_rules.py v3 - context-aware scam-pattern detector (Hindi / Marathi / Hinglish / English)
import unicodedata

SIGNALS = {
    "authority_claim": {
        "weight": 2,
        "words": ["cbi", "सीबीआई", "सीबीआय", "सी बी आई", "police", "पुलिस", "पोलीस",
                  "enforcement directorate", "प्रवर्तन निदेशालय", "customs",
                  "कस्टम", "narcotics", "नारकोटिक्स", "trai", "ट्राई",
                  "cyber crime", "साइबर क्राइम", "सायबर", "rbi", "आरबीआई",
                  "आर बी आई", "court", "कोर्ट", "न्यायालय", "अधिकारी",
                  "income tax", "इनकम टैक्स", "इन्कम टॅक्स", "fraud department",
                  "फ्रॉड डिपार्टमेंट"],
    },
    "digital_arrest": {   # STRONG
        "weight": 4,
        "words": ["digital arrest", "डिजिटल अरेस्ट", "डिजिटल अटक",
                  "डिजिटल अटकेत", "गिरफ्तार", "अटक", "arrest warrant", "वारंट",
                  "मनी लॉन्ड्रिंग", "मनी लॉन्डरिंग", "money laundering",
                  "illegal items", "illegal parcel", "नशीला", "ड्रग्स", "drugs"],
    },
    "safe_account": {     # STRONG
        "weight": 4,
        "words": ["सुरक्षित खाते", "सुरक्षित अकाउंट", "सुरक्षित खात्यात",
                  "safe account", "आरबीआई खाते", "आरबीआई के खाते"],
    },
    "screen_share": {     # STRONG
        "weight": 4,
        "words": ["स्क्रीन शेयर", "screen share", "anydesk", "teamviewer",
                  "quicksupport", "remote access"],
    },
    "secrecy": {
        "weight": 4,
        "words": ["किसी को मत बताइए", "किसी को न बताएं", "किसी को मत बताना",
                  "कोणाला सांगू नका", "कुणाला सांगू नका", "don't tell anyone",
                  "do not tell anyone", "घरवालों को मत", "परिवार को मत",
                  "कॉल कट मत", "फोन मत काटिए", "कॉल कट करू नका",
                  "confidential", "keep it secret", "गोपनीय", "गुप्त रखें",
                  "सीक्रेट", "secret"],
    },
    "threat": {
        "weight": 2,
        "words": ["कारवाई", "कार्रवाई", "केस दर्ज", "पुलिस केस", "हिरासत",
                  "custody", "ब्लॉक", "block", "कट जाएगा", "बंद हो जाएगा",
                  "बंद होईल", "compromised", "suspended", "फ्रीज", "freeze",
                  "तक्रार आली", "गुन्हा दाखल"],
    },
    "money_demand": {
        "weight": 3,
        "words": ["पैसे ट्रांसफर", "पैसा ट्रांसफर", "पैसे भेज", "पैसा भेज",
                  "पैसे पाठवा", "पैसे पाठव", "ट्रांसफर करो", "ट्रांसफर कर",
                  "ट्रांसफर कीजिए", "ट्रांसफर करना", "transfer", "जमा करना",
                  "verification के लिए", "सत्यापन", "रुपये भेज", "पैसे भरा",
                  "पैसे भर", "delivery charges", "charges first"],
    },
    "advance_fee": {
        "weight": 3,
        "words": ["लॉटरी", "lottery", "इनाम जीता", "प्रोसेसिंग फीस",
                  "processing fee", "रजिस्ट्रेशन फीस", "लकी ड्रॉ", "you won",
                  "prize"],
    },
    "remote_access": {
        "weight": 2,
        "words": ["ऐप डाउनलोड", "एप डाउनलोड", "app download", "install"],
    },
    "urgency": {
        "weight": 2,
        "words": ["अभी", "तुरंत", "लगेच", "आत्ताच", "ताबडतोब", "immediately",
                  "right now", "आज ही", "आज रात", "एक घंटे", "30 मिनट"],
    },
    "sensitive_info": {
        "weight": 3,
        "words": ["otp", "ओटीपी", "ओ टी पी", "पिन नंबर", "पिन बताइए",
                  "pin number", "cvv", "आधार नंबर", "aadhaar", "पासवर्ड",
                  "password", "कार्ड नंबर", "card number",
                  "code you just received", "बैंक बैलेंस"],
    },
}

STRONG = {"digital_arrest", "safe_account", "screen_share"}


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

    n = len(found)                      # how many different kinds of warning sign
    has_strong = any(k in STRONG for k in found)

    if score >= 7 and (n >= 3 or (has_strong and n >= 2)):
        level = "HIGH"
    elif has_strong or (n >= 2 and score >= 4):
        level = "MEDIUM"
    elif score >= 2:
        level = "LOW"
    else:
        level = "NONE"
    return {"level": level, "score": score, "signals": found}