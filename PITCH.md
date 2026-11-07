# Ruko (रुको): a calm voice for scam calls

**Ishwari Walewadikar** · Third-year B.E. Instrumentation, AISSMS Institute of Information Technology, Pune · Solo entry

## The problem
"Digital arrest" scams trap a victim in a frightening call, often a video call, and tell them to stay silent and move money. India recorded 297,727 digital-arrest complaints and ₹4,057.7 crore in losses from 2022 to May 2026 (NewsBytes). In Pune, senior citizens lost about ₹100 crore in 136 cases between January 2025 and July 2026 (Punekar News). Victims are often told not to talk to relatives, so a useful tool must bring family back in.

## The solution
Ruko is a voice-first scam-pause companion for Hindi and Marathi speakers. The user says what the caller is telling them. Ruko turns the speech into text, checks it for known scam signs (fake officials, secrecy, urgent money, link or app requests, card details), and answers in a calm spoken warning. It never says a call is safe.

- **One-tap family alert:** a message goes to one family member on Telegram, only when the user presses the button.
- **"I already sent money":** a short form that builds a summary to read out to the 1930 cyber crime helpline.
- **Practice mode:** families listen to made-up calls and guess scam or normal.
- **Large-text mode** for older users.

## Gnani models used
- **Prisma v2.5** (speech-to-text): transcribes Hindi and Marathi speech. Measured end-to-end latency about 0.2 to 0.4 s.
- **Timbre v2.5** (text-to-speech): speaks the warnings, summaries and practice calls.
- The rest is Python, Streamlit, my own rule-based detector and the Telegram Bot API. No other AI model is used.

## Honest results
Tested only on made-up sentences. On sentences I had not tuned the rules for, the detector caught **2 of 10** and then **4 of 15** scam lines. I improved the rules afterwards, but those later scores are not a fair test, so I do not claim them as accuracy. Keyword rules do not generalise well, and the next step is a model that understands meaning.

## Limits
Ruko cannot hear normal phone calls by itself; the user speaks to it or uses speaker mode. It can miss new scam wording. My Marathi warning text has not been fully reviewed by a native speaker. It is a prototype and does not replace the police, a bank or the 1930 helpline.

## Data
Synthetic sentences and my own recorded voice only. No real phone numbers, accounts or other people's recordings.

**Links:** Landing page https://claude.ai/artifact/GtpTkR1c1WfBEVseDFB2MK · Full test log: `results.md` in this repository.
