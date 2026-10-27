# Ruko (रुको)

A voice-first scam-pause companion for senior citizens in India. Built for the
Great Indian AI Internship Challenge 2026 using Gnani.ai Prisma v2.5 (speech-to-text)
and Timbre v2.5 (text-to-speech).

## Problem
"Digital arrest" and similar coercion scams cost Indian victims thousands of crores,
and seniors are heavily targeted. Victims are told to keep the call secret.

## What Ruko does
1. Listens to a spoken description of the call (Hindi / Marathi).
2. Checks it against known scam patterns.
3. Replies in a calm spoken warning, and points to family and the 1930 helpline.

Ruko never says a call is "safe". It only reports known warning signs.

## Run it
    python -m pip install -r requirements.txt
    copy .env.example .env      (then put your own Gnani API key inside .env)
    python -m streamlit run app.py

## Data
Only synthetic or self-recorded test data. No real phone numbers, accounts or recordings.

## Status
See `results.md` for daily test results and known limitations.

## Known limitations
- Cannot listen to normal phone calls by itself. The user speaks to Ruko or uses speaker mode.
- Scam detection is keyword-and-context based. On a first fair test with sentences I had not seen, it caught 2/10 scams and flagged 3/7 normal lines. After tuning it improved, but that second result is not a fair test.
- Marathi warning text has not been fully reviewed by a native speaker.
- The family alert goes to one fixed Telegram contact and only when the user presses the button.
- Not a replacement for police, banks or the 1930 helpline.