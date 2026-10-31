# Ruko - Test Results Log

Project: voice-first scam-pause companion (Hindi / Marathi) for the Great Indian AI Internship Challenge 2026
Models: Gnani.ai Prisma v2.5 (speech-to-text), Timbre v2.5 (text-to-speech)
Deadline: 10 Nov 2026, 11:59 PM IST

Everything inside a code block is real terminal output. Anything shown as ___ is not recorded yet and will be filled in, not guessed.

---

## 24 Oct 2026 - Day 1

**Setup**
- Gnani API key created. Credits at start: 4.9k / 5k.
- Python 3.14 venv working. Key check printed `Key found!`.
- Fixed: `pip.exe` was blocked by a Windows policy, so I used `python -m pip install requests python-dotenv`.
- Fixed: VS Code play button used the wrong Python (`ModuleNotFoundError: No module named 'requests'`). Now I run `python file.py` in the terminal with `(venv)` on.

```
Program 'pip.exe' failed to run: An Application Control policy has blocked this file
Successfully installed certifi-2026.10.23 charset_normalizer-3.5.2 idna-3.20 python-dotenv-1.2.4 requests-2.34.2 urllib3-2.8.0
Key found!
```

**Text-to-speech (Timbre v2.5), errors found and fixed**

```
Status: 400
{"success":false,"message":"'model' is required. The supported models are \"timbre-v2.5\", \"timbre-v3.0\". See https://docs.gnani.ai/api/TTS/tts-inference for the current models and voices.","status_code":400}
```

```
Status: 400
{"success":false,"message":"Invalid request: Value error, Voice 'Karan' is not supported by model 'timbre-v2.5'. Supported voices: Nalini, Bhavna, Yashvi, Urmila, Jwala, Chitra, Ambuja, Deepak, Roopesh, Vikrant, Hemraj, Jalaj, Omkar, Aarohi, Bhavini, Charvi, Eishani, Falguni, Gauri, Iravati, Janaki, Kamakshi, Madhuri, Radhika, Shweta, Tanvi, Vidya, Wamika, Yamini, Abhimanyu, Chirag, Deven, Farhan, Jatin, Kartik, Kaveri, Trupti, Devika, Pranav, Shlok, Girish, Asmita, Trisha, Brinda, Vedika, Noopur, Oviya, Parvati, Suhana, Lehara, Lavanya, Yukti, Varuni, Saanvi, Kavin, Hansika, Reshma, Riyaan, Zahira, Ishaan, Kirra, Dhruva, Damini, Urvashi, Falak, Veera, Lalita, Nayana, Gaurav, Harshit, Mehuli, Zayan, Poorvi at body","status_code":400}
```

```
Status: 200
Saved reply.wav - open it and listen!
```

- The saved file (285 KB) would not play: the request had no `language` and no `audio_config`, so the audio had no WAV header. Added `language`, `speed` 0.9 and `audio_config` (24000 Hz, mono, 16-bit, wav). Then it played.
- Voice quality notes: ___

**Speech-to-text (Prisma v2.5) on `reply.wav`**

```
Status: 200
{"success":true,"request_id":"01a16e34-d818-77a6-b127-39e250b19c45","transcript":"यह एक धोखाधड़ी का कॉल हो सकता है, पैसे मत भेजिए।","model":"gnani-prisma-v2.5","processing_time":0.15277767181396484,"end_to_end_latency":0.17606163024902344,"output":{"literal":"यह एक धोखाधड़ी का कॉल हो सकता है, पैसे मत भेजिए।"}}
```

- Result: transcript matched exactly. End-to-end latency 0.176 s.

**First scam detector (rules v1), three lines**

```
मैं CBI से बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसे ट्रांसफर करो
  -> {'level': 'HIGH', 'score': 15, 'signals': {'authority_claim': ['cbi'], 'digital_arrest': ['डिजिटल अरेस्ट'], 'secrecy': ['किसी को मत बताइए'], 'money_demand': ['पैसे ट्रांसफर', 'ट्रांसफर करो'], 'urgency': ['अभी']}}
आपका बैंक OTP शेयर कीजिए तुरंत
  -> {'level': 'MEDIUM', 'score': 5, 'signals': {'urgency': ['तुरंत'], 'sensitive_info': ['otp']}}
Hello, your courier will arrive tomorrow
  -> {'level': 'NONE', 'score': 0, 'signals': {}}
```

**Full pipeline (audio -> text -> rules -> spoken warning), same scam audio run twice**

```
1. Listening...
   Heard: मैं सी बी आई से बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसे ट्रांसफ़र करो।
2. Checking...
   Level: HIGH | Score: 10
   Signals: ['digital_arrest', 'secrecy', 'urgency']
3. Speaking warning...
   Saved: warning.wav
```

```
1. Listening...
   Heard: मैं सीबीआई से बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसे ट्रांसफर करो।
2. Checking...
   Level: HIGH | Score: 13
   Signals: ['digital_arrest', 'secrecy', 'money_demand', 'urgency']
3. Speaking warning...
   Saved: warning.wav
```

```
1. Listening...
   Heard: नमस्ते, आपका कूरियर कल सुबह 10:00 बजे पहुँच जाएगा।
2. Checking...
   Level: NONE | Score: 0
   Signals: []
3. Speaking warning...
   Saved: warning.wav
```

- Bug found: the same sentence scored 10 and 13 because the speech-to-text spells words differently each time, and my keyword was "cbi" in English letters.
- Fix: text normalisation (lowercase, remove the nukta dot) plus Devanagari spellings (सीबीआई, सी बी आई). After the fix both spellings gave the same result:

```
मैं सीबीआई से बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसे ट्रांसफर करो।
  -> {'level': 'HIGH', 'score': 15, 'signals': {'authority_claim': ['सीबीआई', 'सी बी आई'], 'digital_arrest': ['डिजिटल अरेस्ट'], 'secrecy': ['किसी को मत बताइए'], 'money_demand': ['पैसे ट्रांसफर', 'ट्रांसफर करो', 'ट्रांसफर कर'], 'urgency': ['अभी']}}
आपका बैंक OTP शेयर कीजिए तुरंत
  -> {'level': 'MEDIUM', 'score': 5, 'signals': {'urgency': ['तुरंत'], 'sensitive_info': ['otp']}}
नमस्ते, आपका कूरियर कल सुबह 10:00 बजे पहुँच जाएगा।
  -> {'level': 'NONE', 'score': 0, 'signals': {}}
I called you while shopping, I need a ride
  -> {'level': 'NONE', 'score': 0, 'signals': {}}
```

**Real-voice test (my own Hindi voice note, WhatsApp .ogg, 24 KB, no conversion needed)**

```
...करो।","model":"gnani-prisma-v2.5","processing_time":0.36752748489379883,"end_to_end_latency":0.3901493549346924,"output":{"literal":"मैं पुलिस बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसा ट्रांसफ़र करो।"}}

Heard: मैं पुलिस बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसा ट्रांसफ़र करो।
Result: {'level': 'HIGH', 'score': 15, 'signals': {'authority_claim': ['पुलिस'], 'digital_arrest': ['डिजिटल अरेस्ट'], 'secrecy': ['किसी को मत बताइए'], 'money_demand': ['ट्रांसफर करो', 'ट्रांसफर कर'], 'urgency': ['अभी']}}
```

- Latency about 0.39 s. STT wrote "पैसा" where my keyword list had "पैसे", so I added "पैसा ट्रांसफर" and "पैसा भेज".
- What I actually said, word for word: ___

---

## 25 Oct 2026 - Day 2

**30-line test (`evaluate.py`): 20 made-up scam lines, 10 made-up normal lines**

Rules v2, before tuning:

```
Scam lines caught (MEDIUM or HIGH): 16/20  (80%)
Normal lines wrongly flagged:       0/10

--- MISSED SCAMS ---
LOW 3 | सत्यापन के लिए अपने खाते का सारा पैसा सुरक्षित खाते में ट्रांसफर कीजिए।
LOW 3 | आपको लॉटरी लगी है, पैसे लेने के लिए पहले एक हजार रुपये ट्रांसफर करें।
LOW 2 | Your parcel has illegal items, speak to the police officer on this video call and keep it confidential.
NONE 0 | अपने फोन में यह ऐप डाउनलोड कीजिए और स्क्रीन शेयर कीजिए ताकि हम आपका खाता सुरक्षित कर सकें।

--- FALSE ALARMS ---
```

After adding safe-account, advance-fee and remote-access signals (tuned on the same lines, so NOT a fair test):

```
Scam lines caught (MEDIUM or HIGH): 20/20  (100%)
Normal lines wrongly flagged:       0/10

--- MISSED SCAMS ---

--- FALSE ALARMS ---
```

**First truly unseen test (17 new lines, rules v2): the honest result**

```
--- NORMAL LINES ---
FALSE ALARM MEDIUM 4 | बैंक का नया ऐप डाउनलोड कीजिए, इसमें पासबुक देख सकते हैं।
FALSE ALARM MEDIUM 4 | यह बात गोपनीय रखिएगा, कल बर्थडे पार्टी सरप्राइज़ है।
OK          LOW 2 | मुझे पुलिस स्टेशन जाना है, गुम हुए मोबाइल की रिपोर्ट लिखवानी
FALSE ALARM MEDIUM 4 | स्कूल में रैफल लॉटरी का ड्रॉ कल है, तुम आओगे?
OK          LOW 3 | Please transfer the notes to my email, I'll check tonight.
OK          NONE 0 | आपला पार्सल उद्या येईल, कृपया घरी राहा.
OK          NONE 0 | डिजिटल इंडिया की नई योजना के बारे में खबर देखी?

UNSEEN: scams caught 2/10, normal lines wrongly flagged 3/7
```

(The scam-lines part scrolled off the terminal and was not copied. The summary line is the real result.)

- Result: 2/10 scams caught, 3/7 normal lines wrongly flagged.
- Cause: keyword matching does not generalise; single words like "app download", "confidential" and "lottery" gave false alarms.
- Fix: rules v3, with context logic (a warning needs two kinds of sign unless a strong sign is present). Re-run on the same 17 lines, NOT a fair test because I edited the rules after seeing the misses:

```
--- NORMAL LINES ---
OK          LOW 2 | बैंक का नया ऐप डाउनलोड कीजिए, इसमें पासबुक देख सकते हैं।
OK          LOW 4 | यह बात गोपनीय रखिएगा, कल बर्थडे पार्टी सरप्राइज़ है।
OK          LOW 2 | मुझे पुलिस स्टेशन जाना है, गुम हुए मोबाइल की रिपोर्ट लिखवानी
OK          LOW 3 | स्कूल में रैफल लॉटरी का ड्रॉ कल है, तुम आओगे?
OK          LOW 3 | Please transfer the notes to my email, I'll check tonight.
OK          NONE 0 | आपला पार्सल उद्या येईल, कृपया घरी राहा.
OK          NONE 0 | डिजिटल इंडिया की नई योजना के बारे में खबर देखी?

UNSEEN: scams caught 9/10, normal lines wrongly flagged 0/7
```

**Other**
- Streamlit server started: `Local URL: http://localhost:8501`.
- `marathi.ogg` test was INVALID: the file was a copy of my Hindi voice note (24,195 bytes, same time stamp as mytest.ogg). Real Marathi test is still to do.
- Git: audio files were pushed by mistake. Fixed `.gitignore` and removed audio from tracking.

---

## 26 Oct 2026 - Day 3

- Added family alert via Telegram bot. User presses a button, one message goes to one contact. Works (message arrived).
- Marathi browser test: said "___", heard "___", level ___.
- Limitation: demo uses one fixed contact; the family member must have started the bot.
- Safety rule: Ruko never sends an alert on its own, only when the user presses the button.

---

## 27 Oct 2026 - Day 4

- Added Practice tab (6 made-up calls; user guesses scam or normal, Ruko explains why) and the "I already sent money" tab (builds a summary to read to the 1930 helpline, fake data only).
- Streamlit error: `alert.py` was missing or empty.

```
ModuleNotFoundError: No module named 'alert'
File "C:\Users\ISHWARI WALEWADIKAR\Ruko\ruko\app.py", line 7, in <module>
    from alert import send_family_alert
```

- Fix: created the file. Check afterwards:

```
-a----        27-10-2026  09:17 PM           1780 alert.py
-a----        26-10-2026  10:31 PM           3289 practice.py
```

- Practice tab result when I tried it: ___

---

## 28 Oct 2026 - Day 5

- Added large-text mode, Streamlit theme (`.streamlit/config.toml`) and a landing page for Ruko (private link).
- User test with ___ (relation / age): hesitated at ___, understood ___, said ___.
- Credits left: ___

---

## 31 Oct 2026 - Fair test on 23 new lines (rules v3)

These 23 sentences were written by an AI assistant, not by an independent person, so the test is not fully independent. Rules were not edited before this run.

```
--- SCAM LINES ---
MISS NONE 0 | Hello sir, aapke naam se ek parcel Mumbai airport par pakda 
MISS LOW 2 | आपकी बिजली का बिल पिछले महीने का बाकी है, आज रात नौ बजे तक न
OK   HIGH 7 | तुमचा मुलगा पोलीस ठाण्यात आहे, त्याला सोडवायचे असेल तर लगेच 
MISS NONE 0 | मैडम, आपका केवाईसी अपडेट नहीं हुआ है, एक लिंक भेज रहा हूँ, उ
MISS LOW 2 | आप पर मुंबई क्राइम ब्रांच में केस दर्ज हुआ है, जब तक जांच पू
MISS NONE 0 | Congratulations madam, you have been selected for a work fro
MISS NONE 0 | आपके आधार कार्ड का इस्तेमाल एक बैंक खाता खोलने में हुआ है जि
MISS LOW 3 | दादाजी, मैं आपका पोता बोल रहा हूँ, मेरा एक्सीडेंट हो गया है,
MISS LOW 2 | तुमचे सिम कार्ड आज रात बंद होणार आहे, ते चालू ठेवायचे असेल त
MISS LOW 2 | This is SBI customer care, your debit card will be blocked i
MISS LOW 3 | आपने कोई लकी ड्रॉ जीता है, गाड़ी मिलेगी, बस टैक्स के नाम पर 
OK   MEDIUM 6 | ईडी का अधिकारी बोल रहा हूँ, आपके खाते में संदिग्ध पैसा आया ह
MISS LOW 2 | मी कुरिअर कंपनीतून बोलतोय, तुमच्या पार्सलमध्ये ड्रग्ज सापडले
OK   MEDIUM 6 | आपका पुराना केस अब कोर्ट पहुँच गया है, गिरफ्तारी से बचना है 
OK   HIGH 9 | सर, आपका इनकम टैक्स रिफंड अटका है, उसे निकालने के लिए अपना न

--- NORMAL LINES ---
OK          NONE 0 | आपके खाते से पाँच सौ रुपये का ट्रांजैक्शन हुआ है। अगर यह आपन
OK          LOW 2 | पापा, पुलिस वाले अंकल स्कूल आए थे और बच्चों को सड़क सुरक्षा 
OK          LOW 3 | कृपया अपना ओटीपी किसी के साथ साझा न करें, बैंक कभी आपसे यह न
OK          LOW 2 | भाई, खाने के पैसे मैं अभी फोन पे कर देता हूँ, तू बस रसीद रख 
OK          NONE 0 | उद्या सकाळी आठ वाजता शाळेची फी भरायची आहे, आठवण करून देतो.
OK          NONE 0 | Your Amazon order has been shipped and will be delivered by 
FALSE ALARM MEDIUM 6 | मौसी का फोन आया था, कल दोपहर को घर आ रही हैं, यह बात अभी किस
OK          NONE 0 | बिजली विभाग का कर्मचारी मीटर रीडिंग लेने कल आएगा, कृपया दरवा

FRESH: scams caught 4/15, normal lines wrongly flagged 1/8
```

- Honest result for v3 on fresh lines: 4/15 scams caught (27%), 1/8 normal lines wrongly flagged.

---

## 31 Oct 2026 - Rules v4 (patterns added after seeing the misses above)

Because v4 was edited after seeing these lines, the numbers below are NOT a fair test.

Same 23 fresh lines:

```
--- SCAM LINES ---
OK   MEDIUM 6 | Hello sir, aapke naam se ek parcel Mumbai airport par pakda 
OK   MEDIUM 4 | आपकी बिजली का बिल पिछले महीने का बाकी है, आज रात नौ बजे तक न
OK   HIGH 15 | तुमचा मुलगा पोलीस ठाण्यात आहे, त्याला सोडवायचे असेल तर लगेच 
OK   MEDIUM 6 | मैडम, आपका केवाईसी अपडेट नहीं हुआ है, एक लिंक भेज रहा हूँ, उ
OK   HIGH 12 | आप पर मुंबई क्राइम ब्रांच में केस दर्ज हुआ है, जब तक जांच पू
MISS LOW 3 | Congratulations madam, you have been selected for a work fro
OK   HIGH 10 | आपके आधार कार्ड का इस्तेमाल एक बैंक खाता खोलने में हुआ है जि
OK   HIGH 11 | दादाजी, मैं आपका पोता बोल रहा हूँ, मेरा एक्सीडेंट हो गया है,
OK   HIGH 11 | तुमचे सिम कार्ड आज रात बंद होणार आहे, ते चालू ठेवायचे असेल त
OK   HIGH 9 | This is SBI customer care, your debit card will be blocked i
OK   MEDIUM 6 | आपने कोई लकी ड्रॉ जीता है, गाड़ी मिलेगी, बस टैक्स के नाम पर 
OK   HIGH 8 | ईडी का अधिकारी बोल रहा हूँ, आपके खाते में संदिग्ध पैसा आया ह
OK   MEDIUM 6 | मी कुरिअर कंपनीतून बोलतोय, तुमच्या पार्सलमध्ये ड्रग्ज सापडले
OK   HIGH 10 | आपका पुराना केस अब कोर्ट पहुँच गया है, गिरफ्तारी से बचना है 
OK   HIGH 9 | सर, आपका इनकम टैक्स रिफंड अटका है, उसे निकालने के लिए अपना न

--- NORMAL LINES ---
OK          NONE 0 | आपके खाते से पाँच सौ रुपये का ट्रांजैक्शन हुआ है। अगर यह आपन
OK          LOW 2 | पापा, पुलिस वाले अंकल स्कूल आए थे और बच्चों को सड़क सुरक्षा 
OK          LOW 3 | कृपया अपना ओटीपी किसी के साथ साझा न करें, बैंक कभी आपसे यह न
OK          NONE 0 | भाई, खाने के पैसे मैं अभी फोन पे कर देता हूँ, तू बस रसीद रख 
OK          NONE 0 | उद्या सकाळी आठ वाजता शाळेची फी भरायची आहे, आठवण करून देतो.
OK          NONE 0 | Your Amazon order has been shipped and will be delivered by 
OK          LOW 4 | मौसी का फोन आया था, कल दोपहर को घर आ रही हैं, यह बात अभी किस
OK          NONE 0 | बिजली विभाग का कर्मचारी मीटर रीडिंग लेने कल आएगा, कृपया दरवा

FRESH: scams caught 14/15, normal lines wrongly flagged 0/8
```

Old 30 lines (also tuned, not fair):

```
Scam lines caught (MEDIUM or HIGH): 20/20  (100%)
Normal lines wrongly flagged:       0/10

--- MISSED SCAMS ---

--- FALSE ALARMS ---
```

The 17 earlier lines (already seen, not fair):

```
--- SCAM LINES ---
OK   MEDIUM 6 | आपके आधार से जुड़े सिम कार्ड से अश्लील संदेश भेजे गए हैं, मु
OK   MEDIUM 6 | तुमच्या मोबाईल नंबरवर तक्रार आली आहे, सीबीआय अधिकारी तुमच्या
OK   MEDIUM 6 | Congratulations, you won a prize, pay the delivery charges f
OK   MEDIUM 4 | आपका बिजली कनेक्शन आज रात कट जाएगा, इस नंबर पर तुरंत कॉल करक
OK   HIGH 7 | आपके पैकेज में नशीला पदार्थ मिला है, जांच के लिए आपको अपना ब
OK   HIGH 7 | Sir, I am calling from your bank's fraud department, your ac
OK   MEDIUM 5 | आपका ATM कार्ड ब्लॉक हो गया है, कार्ड नंबर और पिन बताइए।
OK   HIGH 13 | मी इन्कम टॅक्स अधिकारी बोलतोय, तुमच्यावर कारवाई होईल, ताबडतो
OK   HIGH 7 | आपका बेटा हमारी हिरासत में है, उसे छुड़ाना है तो अभी दो लाख 
OK   MEDIUM 6 | ऑनलाइन नौकरी के लिए पहले रजिस्ट्रेशन के पाँच हजार रुपये भेजि

--- NORMAL LINES ---
OK          LOW 3 | बैंक का नया ऐप डाउनलोड कीजिए, इसमें पासबुक देख सकते हैं।
OK          LOW 4 | यह बात गोपनीय रखिएगा, कल बर्थडे पार्टी सरप्राइज़ है।
OK          LOW 2 | मुझे पुलिस स्टेशन जाना है, गुम हुए मोबाइल की रिपोर्ट लिखवानी
OK          LOW 3 | स्कूल में रैफल लॉटरी का ड्रॉ कल है, तुम आओगे?
OK          NONE 0 | Please transfer the notes to my email, I'll check tonight.
OK          NONE 0 | आपला पार्सल उद्या येईल, कृपया घरी राहा.
OK          NONE 0 | डिजिटल इंडिया की नई योजना के बारे में खबर देखी?

UNSEEN: scams caught 10/10, normal lines wrongly flagged 0/7
```

- Known remaining miss: the work-from-home registration-fee scam line still scores LOW.

---

## 31 Oct 2026 - Sentence from a friend (first test of v4 on text I had not seen)

A friend wrote this Marathi family-emergency scam line. It arrived after v4 was finished and I did not edit any rule before running it.

```
हॅलो , मी तुमच्या मुलाचा मित्र  बोलत आहे . त्याचा एका ठिकाणी accident झाला आहे आणि त्याला हॉस्पिटल मध्ये न्यायचं आहे त्यामुळं मला ह्या नंबर वर पैसे पाठवा .
```

```
(venv) PS C:\Users\ISHWARI WALEWADIKAR\Ruko\ruko> python evaluate_fresh2.py
--- SCAM LINES ---
OK   MEDIUM 5 | (the friend's sentence)

--- NORMAL LINES ---

FRESH2: scams caught 1/1, normal lines wrongly flagged 0/0
```

- Result: caught, MEDIUM, score 5. This is one sentence, so it is not an accuracy percentage. More sentences from friends are needed.

---

## Summary table of all rule tests

| Rules | Test set | Scams caught | Normal lines flagged | Fair test? |
|---|---|---|---|---|
| v2 | 30 lines I wrote | 16/20 | 0/10 | Yes (first run) |
| v2 | 17 new lines | 2/10 | 3/7 | Yes |
| v3 | same 17 lines after edits | 9/10 | 0/7 | No, tuned |
| v3 | 23 fresh lines (AI-written) | 4/15 | 1/8 | Yes |
| v4 | same 23 lines after edits | 14/15 | 0/8 | No, tuned |
| v4 | old 30 lines | 20/20 | 0/10 | No, tuned |
| v4 | 17 earlier lines | 10/10 | 0/7 | No, tuned |
| v4 | friend's sentence (`evaluate_fresh2.py`) | 1/1 | 0/0 | Yes, but only one sentence |

Conclusion so far: keyword and context rules do not generalise well to unseen scam wording (2/10 and 4/15 on genuinely unseen sets). Tuned scores are higher but are not evidence of real accuracy. Next step: more fresh sentences from friends, and a model that understands meaning if the challenge rules allow one.

---

## Still to record

- [ ] Marathi app test (what I said, heard, level, voice quality)
- [ ] More friend sentences in `evaluate_fresh2.py` (at least 10 scam and 5 normal)
- [ ] Noisy-audio test and normal-call voice test
- [ ] Real-user test with a parent or grandparent
- [ ] Native-speaker review of the Marathi warning text
- [ ] Credits left on the Gnani Usage page
- [ ] Challenge rule on non-Gnani language models
- [ ] Screenshots of the Practice tab and the Telegram alert for the demo

## Problems found and fixed

1. Windows blocked `pip.exe`; used `python -m pip`.
2. VS Code play button used the wrong Python; run scripts from the terminal with the venv on.
3. TTS API needed `model`, `language` and `audio_config`; "Karan" was not a valid voice for timbre-v2.5.
4. STT writes "CBI" in Devanagari and varies spelling; fixed with text normalisation.
5. Keyword rules overfit; honest unseen results were 2/10 and 4/15.
6. `alert.py` was missing, causing an import error in Streamlit; fixed by creating the file.
7. Audio files were pushed to Git by mistake; fixed `.gitignore`.

## Limits (honest)

- Ruko cannot listen to normal phone calls by itself; the user speaks to it or uses speaker mode.
- It never says a call is safe; it only reports known warning signs.
- Detection can miss new wording.
- Marathi warning text was written by me and is not yet reviewed by a native speaker.
- The family alert goes to one fixed Telegram contact and only when the user presses the button.
- Prototype only; not a replacement for the police, a bank or the 1930 helpline.