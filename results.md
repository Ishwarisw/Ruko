# Ruko - Test Results Log

## 24 Oct 2026 - Day 1

**Setup**
- Gnani API key created. Python 3.14 venv working.
- Fixed: pip.exe was blocked by Windows policy, used `python -m pip` instead.
- Fixed: TTS needed `model`, `language` and `audio_config` fields, and voice "Karan" did not exist for timbre-v2.5 (used "Nalini" / "Deepak").

**Speech-to-text (Prisma v2.5)**
- Transcribed synthetic Hindi audio correctly.
- Latency: about 0.18 seconds end to end.

**Text-to-speech (Timbre v2.5)**
- Voice: Nalini / Deepak, speed 0.9.
- Audio quality notes: (write what you heard here)

**Scam detector (rules)**
- Problem found: STT writes "CBI" in Devanagari ("सी बी आई" / "सीबीआई") and varies spelling (ट्रांसफ़र vs ट्रांसफर), so keyword matching missed some signals.
- Fix: text normalisation plus Devanagari keyword variants.
- Result after fix:
  - Fake scam call: HIGH (score 15)
  - OTP demand: MEDIUM (score 5)
  - Courier message: NONE (score 0)
  - "called / shopping" sentence: NONE (score 0)

**Still to test**
- My own recorded voice (Hindi)
- Marathi
- 30 synthetic call scripts (20 scam, 10 normal)
- Noisy audio

## 24 Oct 2026 - Real voice test
- Source: my own voice, WhatsApp voice note (.ogg, 24 KB), Hindi. Accepted directly by Prisma STT, no conversion needed.
- Latency: ~0.39 s end to end.
- Heard: "मैं पुलिस बोल रहा हूँ, आप डिजिटल अरेस्ट में हैं, किसी को मत बताइए और अभी पैसा ट्रांसफ़र करो।"
- Level: HIGH (15).
- Issue: STT wrote "पैसा" where I said "पैसे" (or similar), so one money keyword missed. Added variants.
- Limitation: single speaker, quiet room, one sentence. Needs noisy and multi-speaker tests.

## 24 Oct 2026 - End of Day 1
- Built: voice pipeline (STT -> scam rules -> TTS), rule file with normalisation, messages in Hindi and Marathi, Streamlit mic screen.
- Real-voice test (Hindi, WhatsApp .ogg): HIGH (15), latency ~0.39 s.
- Found: STT writes "पैसा" for "पैसे" -> added keyword variants.
- Marathi messages written by me, need a native-speaker review.
- Credits used so far: (check the Usage page and write the number)
- Streamlit: installed / blocked (write which)


## 25 Oct 2026 - Day 2
- 30-line test, before tuning: scams caught 16/20, normal lines flagged 0/10.
- Missed: safe-account transfer, lottery advance fee, English "illegal items/confidential", app download + screen share.
- Added signals: safe_account, advance_fee, remote_access; more secrecy/money words.
- After tuning: caught __/20, false alarms __/10. NOTE: tuned on same lines, so not a fair test. Need unseen set.
- Marathi voice test: NOT done yet (marathi.ogg was a copy of the Hindi file).
- Git: audio had been committed by mistake; fixed .gitignore and removed from tracking

## 26 Oct 2026 - Day 3
- Added family alert via Telegram bot. User presses a button, one message goes to one contact. Works.
- Marathi browser test: said "...", heard "...", level ___.
- Limitation: demo uses one fixed contact; the family member must have started the bot.
- Safety rule: Ruko never sends an alert on its own, only when the user presses the button..

## 28 Oct 2026 - Day 5
- Added large-text mode.
- Fresh-set result: scams caught __/__, false alarms __/__ (rules untouched before this run).
- User test with ___ (relation/age): hesitated at ___, understood ___, said ___.
- Credits left: ____