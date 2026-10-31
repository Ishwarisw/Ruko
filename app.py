# app.py - Ruko: check a call, family alert, 1930 helper, practice mode
import streamlit as st
from gnani_client import transcribe_bytes, speak_bytes
from scam_rules import check
from messages import MESSAGES
from summary_1930 import build_summary
from alert import send_family_alert
from practice import PRACTICE

st.set_page_config(page_title="Ruko", page_icon="🛑")

st.markdown("# 🛑 रुको। पहले पूछो।")
st.markdown("**A calm voice that warns you about scam calls.** Demo uses made-up data only.")

lang_label = st.selectbox("Language / भाषा", ["हिंदी (Hindi)", "मराठी (Marathi)"])
code = "hi-IN" if "Hindi" in lang_label else "mr-IN"

big = st.toggle("🔍 Large text (बड़े अक्षर)", value=True)
if big:
    st.markdown(
        """
        <style>
        html, body, [class*="css"], p, label, li { font-size: 22px !important; }
        h1 { font-size: 2.4rem !important; }
        h3 { font-size: 1.8rem !important; }
        .stButton > button {
            font-size: 24px !important;
            padding: 0.8rem 1.4rem !important;
            border-radius: 12px !important;
            width: 100%;
        }
        .stTabs [data-baseweb="tab"] { font-size: 20px !important; padding: 12px 18px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def cached_voice(text, voice, lang):
    """Remember generated audio so repeated clicks do not use more credits."""
    return speak_bytes(text, language=lang, voice=voice)


tab1, tab2, tab3 = st.tabs(["🎤 Check a call", "🚨 I already sent money", "🎯 Practice"])

# ---------------------------------------------------------------- Tab 1
with tab1:
    st.write("Press the mic, say what the caller is telling you, then press Stop.")
    recorded = st.audio_input("Record")
    uploaded = st.file_uploader("...or upload a voice note", type=["wav", "ogg", "mp3", "m4a"])
    audio = recorded or uploaded

    if audio is not None and st.button("Check this call"):
        try:
            with st.spinner("Listening..."):
                text = transcribe_bytes(audio.getvalue(), audio.name or "audio.wav", code)
            result = check(text)
            message = MESSAGES[code][result["level"]]
            with st.spinner("Preparing voice..."):
                wav = speak_bytes(message, language=code)
            st.session_state["last"] = {
                "text": text, "result": result, "message": message, "wav": wav, "code": code,
            }
            st.session_state.pop("alert_status", None)
        except Exception as e:
            st.error(f"Something went wrong: {e}")

    last = st.session_state.get("last")
    if last:
        level = last["result"]["level"]
        colors = {"HIGH": "red", "MEDIUM": "orange", "LOW": "blue", "NONE": "gray"}
        st.subheader("What I heard")
        st.write(last["text"])
        st.markdown(f"### Risk level: :{colors[level]}[{level}]")
        if last["result"]["signals"]:
            st.write("Warning signs found:", ", ".join(last["result"]["signals"].keys()))
        st.info(last["message"])
        st.audio(last["wav"], format="audio/wav")

        if level in ("HIGH", "MEDIUM"):
            st.write("Want a family member to know right now?")
            if st.button("📲 Alert my family"):
                ok, msg = send_family_alert(level, last["text"], last["code"])
                st.session_state["alert_status"] = (ok, msg)
            status = st.session_state.get("alert_status")
            if status:
                (st.success if status[0] else st.error)(status[1])

        st.warning("Ruko cannot prove a call is safe. If anyone asks for money or secrecy, "
                   "stop and call your family or 1930.")

# ---------------------------------------------------------------- Tab 2
with tab2:
    st.error("Call **1930** (cyber crime helpline) right now. Do not wait. "
             "Fill this in first so you can read it out.")
    st.caption("Use fake data in this demo. Nothing is saved or sent.")
    when = st.text_input("When did you send the money? (date and time)")
    amount = st.text_input("Amount (rupees)")
    how = st.selectbox("How did you send it?", ["UPI", "Bank transfer", "Card", "Cash / other"])
    txn = st.text_input("Transaction ID (from your payment app)")
    receiver = st.text_input("Account number or UPI ID the money went to")
    claim = st.text_input("Who did the caller say they were?")
    number = st.text_input("Caller's phone number")

    if st.button("Make my 1930 summary"):
        summary = build_summary(code, when or "-", amount or "-", how, txn or "-",
                                receiver or "-", claim or "-", number or "-")
        st.text_area("Read this to the operator", summary, height=260)
        try:
            with st.spinner("Preparing voice..."):
                wav = speak_bytes(summary, language=code)
            st.audio(wav, format="audio/wav")
        except Exception as e:
            st.error(f"Voice failed: {e}")
        st.download_button("Download as text", summary, file_name="summary_1930.txt")

# ---------------------------------------------------------------- Tab 3
with tab3:
    st.write("Listen to a made-up call and decide: **scam or normal?** "
             "Practising when you are calm helps when a real call comes.")
    st.caption("All calls are synthetic. Audio is generated once and reused.")

    names = [p["title"] for p in PRACTICE]
    choice = st.selectbox("Choose a call", names)
    item = PRACTICE[names.index(choice)]

    if st.button("▶ Play this call"):
        try:
            with st.spinner("Preparing call..."):
                st.session_state["practice_audio"] = cached_voice(item["text"], item["voice"], "hi-IN")
                st.session_state["practice_for"] = choice
        except Exception as e:
            st.error(f"Voice failed: {e}")

    if st.session_state.get("practice_for") == choice:
        st.audio(st.session_state["practice_audio"], format="audio/wav")

    guess = st.radio("What do you think?", ["Scam", "Normal"], horizontal=True, index=None)
    if guess and st.button("Show the answer"):
        correct = (guess == "Scam") == item["is_scam"]
        if correct:
            st.success("Correct! Well done.")
        else:
            st.error("Not this time, and that is okay. This is how we learn.")
        st.write("**Why:**", item["why"])
        with st.expander("Transcript"):
            st.write(item["text"])