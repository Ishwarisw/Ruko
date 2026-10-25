# evaluate.py - runs 30 synthetic call lines through the scam detector
# All sentences are made up. No real people, numbers or accounts.
import sys
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

SCAM = [
    "मैं सीबीआई से बोल रहा हूँ, आपके आधार नंबर से मनी लॉन्ड्रिंग हुई है, आप डिजिटल अरेस्ट में हैं।",
    "आपके नाम पर एक पार्सल पकड़ा गया है जिसमें ड्रग्स मिले हैं, कस्टम अधिकारी से बात कीजिए, किसी को मत बताइए।",
    "वीडियो कॉल चालू रखिए, कॉल कट मत कीजिए, वरना आपके खिलाफ वारंट जारी होगा।",
    "सत्यापन के लिए अपने खाते का सारा पैसा सुरक्षित खाते में ट्रांसफर कीजिए।",
    "मी पोलीस बोलतोय, तुमच्या नावावर गुन्हा दाखल झाला आहे, कोणाला सांगू नका.",
    "तुम्ही डिजिटल अटकेत आहात, आत्ताच पैसे पाठवा नाहीतर अटक होईल.",
    "मैं साइबर क्राइम से बोल रहा हूँ, आपका सिम बंद हो जाएगा, तुरंत ओटीपी बताइए।",
    "आरबीआई के खाते में पैसा जमा करना होगा, अभी जमा करना होगा।",
    "This is the Enforcement Directorate, you are under digital arrest, do not tell anyone, transfer money right now.",
    "आपका बैंक खाता फ्रीज होने वाला है, अभी अपना पासवर्ड और ओटीपी बताइए।",
    "Sir, your KYC is expired, install AnyDesk immediately and share the code.",
    "मैं ट्राई से बोल रहा हूँ, आपके नंबर से गैरकानूनी कॉल हुए हैं, पुलिस केस होगा, किसी को न बताएं।",
    "तुमच्या आधार नंबरवरून मनी लॉन्डरिंग झाली आहे, पोलीस तुम्हाला अटक करतील, घरी कोणाला सांगू नका.",
    "कोर्ट का नोटिस आया है, गिरफ्तार होने से बचना है तो अभी पैसे भेजिए।",
    "आपके बेटे का एक्सीडेंट हो गया है, पुलिस केस से बचाने के लिए तुरंत पैसे ट्रांसफर करो, मम्मी को मत बताना।",
    "आपको लॉटरी लगी है, पैसे लेने के लिए पहले एक हजार रुपये ट्रांसफर करें।",
    "मी बँकेतून बोलतोय, तुमचे कार्ड बंद होईल, लगेच ओटीपी सांगा.",
    "Your parcel has illegal items, speak to the police officer on this video call and keep it confidential.",
    "आप पर केस दर्ज है, फोन मत काटिए, जब तक हम न कहें कॉल पर रहिए।",
    "अपने फोन में यह ऐप डाउनलोड कीजिए और स्क्रीन शेयर कीजिए ताकि हम आपका खाता सुरक्षित कर सकें।",
]

NORMAL = [
    "नमस्ते, आपका कूरियर कल सुबह दस बजे पहुँच जाएगा।",
    "मम्मी, मैं शाम को घर आऊँगा, खाना बना कर रखना।",
    "आपका बिजली का बिल इस महीने के अंत तक भरना है।",
    "Hi, I'll call you after lunch.",
    "बैंक की तरफ से सूचना: आपके खाते में वेतन जमा हो गया है।",
    "डॉक्टर ने कहा है कि कल सुबह खाली पेट आना है।",
    "उद्या सकाळी दहा वाजता मीटिंग आहे, वेळेवर या.",
    "पुलिस ने ट्रैफिक चालान की रसीद भेजी है, ऑनलाइन चेक कर लीजिए।",
    "मुझे अभी बाज़ार जाना है, कुछ मंगाना हो तो बताओ।",
    "आधार कार्ड अपडेट के लिए सरकारी केंद्र पर जाइए, कोई ओटीपी किसी को मत दीजिए।",
]

FLAG_LEVELS = ("MEDIUM", "HIGH")   # what counts as "Ruko warns the user"

caught, missed, false_alarms = 0, [], []

for s in SCAM:
    r = check(s)
    if r["level"] in FLAG_LEVELS:
        caught += 1
    else:
        missed.append((s, r))

for s in NORMAL:
    r = check(s)
    if r["level"] in FLAG_LEVELS:
        false_alarms.append((s, r))

print(f"Scam lines caught (MEDIUM or HIGH): {caught}/{len(SCAM)}  ({100*caught//len(SCAM)}%)")
print(f"Normal lines wrongly flagged:       {len(false_alarms)}/{len(NORMAL)}")

print("\n--- MISSED SCAMS ---")
for s, r in missed:
    print(r["level"], r["score"], "|", s)

print("\n--- FALSE ALARMS ---")
for s, r in false_alarms:
    print(r["level"], r["score"], "|", s)