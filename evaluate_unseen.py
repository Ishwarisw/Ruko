# evaluate_unseen.py - sentences written AFTER the rules were tuned. Synthetic only.
import sys
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

SCAM = [
    "आपके आधार से जुड़े सिम कार्ड से अश्लील संदेश भेजे गए हैं, मुंबई पुलिस आपसे बात करेगी, यह बात सीक्रेट रखिए।",
    "तुमच्या मोबाईल नंबरवर तक्रार आली आहे, सीबीआय अधिकारी तुमच्याशी बोलतील, आत्ताच व्हिडिओ कॉलवर या.",
    "Congratulations, you won a prize, pay the delivery charges first through UPI.",
    "आपका बिजली कनेक्शन आज रात कट जाएगा, इस नंबर पर तुरंत कॉल करके बिल अपडेट कीजिए।",
    "आपके पैकेज में नशीला पदार्थ मिला है, जांच के लिए आपको अपना बैंक बैलेंस दिखाना होगा।",
    "Sir, I am calling from your bank's fraud department, your account is compromised, tell me the code you just received.",
    "आपका ATM कार्ड ब्लॉक हो गया है, कार्ड नंबर और पिन बताइए।",
    "मी इन्कम टॅक्स अधिकारी बोलतोय, तुमच्यावर कारवाई होईल, ताबडतोब पैसे भरा, घरी कोणाला सांगू नका.",
    "आपका बेटा हमारी हिरासत में है, उसे छुड़ाना है तो अभी दो लाख रुपये भेजो।",
    "ऑनलाइन नौकरी के लिए पहले रजिस्ट्रेशन के पाँच हजार रुपये भेजिए, फिर घर बैठे कमाइए।",
]

NORMAL = [
    "बैंक का नया ऐप डाउनलोड कीजिए, इसमें पासबुक देख सकते हैं।",
    "यह बात गोपनीय रखिएगा, कल बर्थडे पार्टी सरप्राइज़ है।",
    "मुझे पुलिस स्टेशन जाना है, गुम हुए मोबाइल की रिपोर्ट लिखवानी है।",
    "स्कूल में रैफल लॉटरी का ड्रॉ कल है, तुम आओगे?",
    "Please transfer the notes to my email, I'll check tonight.",
    "आपला पार्सल उद्या येईल, कृपया घरी राहा.",
    "डिजिटल इंडिया की नई योजना के बारे में खबर देखी?",
]

caught = 0
print("--- SCAM LINES ---")
for s in SCAM:
    r = check(s)
    ok = r["level"] in ("MEDIUM", "HIGH")
    caught += ok
    print("OK  " if ok else "MISS", r["level"], r["score"], "|", s[:60])

false_alarms = 0
print("\n--- NORMAL LINES ---")
for s in NORMAL:
    r = check(s)
    bad = r["level"] in ("MEDIUM", "HIGH")
    false_alarms += bad
    print("FALSE ALARM" if bad else "OK         ", r["level"], r["score"], "|", s[:60])

print(f"\nUNSEEN: scams caught {caught}/{len(SCAM)}, normal lines wrongly flagged {false_alarms}/{len(NORMAL)}")