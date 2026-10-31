# evaluate_fresh.py - a NEW unseen set. All sentences are made up. No real people, numbers or accounts.
# Run ONCE and write the result down BEFORE changing any rule.
import sys
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

SCAM = [
    "Hello sir, aapke naam se ek parcel Mumbai airport par pakda gaya hai, usme fake passports hain. Aapko abhi cyber cell se baat karni padegi.",
    "आपकी बिजली का बिल पिछले महीने का बाकी है, आज रात नौ बजे तक नहीं भरा तो कनेक्शन काट दिया जाएगा, इस नंबर पर अभी फोन कीजिए।",
    "तुमचा मुलगा पोलीस ठाण्यात आहे, त्याला सोडवायचे असेल तर लगेच ऑनलाइन पैसे पाठवा आणि आईला काही सांगू नका.",
    "मैडम, आपका केवाईसी अपडेट नहीं हुआ है, एक लिंक भेज रहा हूँ, उस पर अपना कार्ड डिटेल डालिए।",
    "आप पर मुंबई क्राइम ब्रांच में केस दर्ज हुआ है, जब तक जांच पूरी नहीं होती आप कैमरे के सामने बैठे रहिए और किसी से बात मत कीजिए।",
    "Congratulations madam, you have been selected for a work from home job, pay 2000 rupees registration and start earning daily.",
    "आपके आधार कार्ड का इस्तेमाल एक बैंक खाता खोलने में हुआ है जिससे गैरकानूनी लेनदेन हुए, आपको अपनी सारी जमा राशि जांच के लिए हमारे खाते में डालनी होगी।",
    "दादाजी, मैं आपका पोता बोल रहा हूँ, मेरा एक्सीडेंट हो गया है, अस्पताल में पैसे भरने हैं, पापा को मत बताना, जल्दी भेजो।",
    "तुमचे सिम कार्ड आज रात बंद होणार आहे, ते चालू ठेवायचे असेल तर मी सांगतो तो ॲप डाउनलोड करा आणि स्क्रीन दाखवा.",
    "This is SBI customer care, your debit card will be blocked in one hour, please read out the six digit code we have just sent.",
    "आपने कोई लकी ड्रॉ जीता है, गाड़ी मिलेगी, बस टैक्स के नाम पर पंद्रह हजार रुपये पहले भेज दीजिए।",
    "ईडी का अधिकारी बोल रहा हूँ, आपके खाते में संदिग्ध पैसा आया है, खाता सील होगा, आप सारा पैसा सुरक्षित खाते में डाल दीजिए ताकि हम जांच कर सकें।",
    "मी कुरिअर कंपनीतून बोलतोय, तुमच्या पार्सलमध्ये ड्रग्ज सापडले आहेत, आता तुम्हाला मुंबई सायबर पोलिसांशी व्हिडिओ कॉलवर बोलावे लागेल.",
    "आपका पुराना केस अब कोर्ट पहुँच गया है, गिरफ्तारी से बचना है तो आज शाम तक सेटलमेंट के लिए पचास हजार भेज दीजिए।",
    "सर, आपका इनकम टैक्स रिफंड अटका है, उसे निकालने के लिए अपना नेट बैंकिंग पासवर्ड बता दीजिए।",
]

NORMAL = [
    "आपके खाते से पाँच सौ रुपये का ट्रांजैक्शन हुआ है। अगर यह आपने नहीं किया तो बैंक की शाखा में संपर्क करें।",
    "पापा, पुलिस वाले अंकल स्कूल आए थे और बच्चों को सड़क सुरक्षा के बारे में बता रहे थे।",
    "कृपया अपना ओटीपी किसी के साथ साझा न करें, बैंक कभी आपसे यह नहीं पूछता।",
    "भाई, खाने के पैसे मैं अभी फोन पे कर देता हूँ, तू बस रसीद रख लेना।",
    "उद्या सकाळी आठ वाजता शाळेची फी भरायची आहे, आठवण करून देतो.",
    "Your Amazon order has been shipped and will be delivered by Saturday.",
    "मौसी का फोन आया था, कल दोपहर को घर आ रही हैं, यह बात अभी किसी को मत बताना, सबको सरप्राइज़ देना है।",
    "बिजली विभाग का कर्मचारी मीटर रीडिंग लेने कल आएगा, कृपया दरवाज़ा खोल दीजिए।",
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

print(f"\nFRESH: scams caught {caught}/{len(SCAM)}, normal lines wrongly flagged {false_alarms}/{len(NORMAL)}")