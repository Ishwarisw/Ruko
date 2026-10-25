# evaluate_fresh.py - a NEW unseen set. Write these lines WITHOUT looking at scam_rules.py.
# Best: ask 2-3 friends/family to each write 5 scam-style and 3 normal sentences
# (Hindi, Marathi or Hinglish). All made up, no real names/numbers.
import sys
from scam_rules import check

sys.stdout.reconfigure(encoding="utf-8")

SCAM = [
    # "your sentence 1",
    # "your sentence 2",
]

NORMAL = [
    # "normal sentence 1",
    # "normal sentence 2",
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