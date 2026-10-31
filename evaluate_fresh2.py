# evaluate_fresh2.py - sentences written by friends/family. Run ONCE, record the result,
# and do NOT edit scam_rules.py before recording it.
import sys
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

SCAM = [
    "हॅलो , मी तुमच्या मुलाचा मित्र  बोलत आहे . त्याचा एका ठिकाणी accident झाला आहे आणि त्याला हॉस्पिटल मध्ये न्यायचं आहे त्यामुळं मला ह्या नंबर वर पैसे पाठवा .",
    # add more scam sentences from friends here, one per line, in quotes, with a comma
]

NORMAL = [
    # add normal sentences from friends here (for example a real bank alert, a family call)
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

print(f"\nFRESH2: scams caught {caught}/{len(SCAM)}, normal lines wrongly flagged {false_alarms}/{len(NORMAL)}")