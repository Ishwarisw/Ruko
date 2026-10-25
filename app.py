# app.py - Ruko screen: speak -> check -> spoken warning, plus 1930 helper
import streamlit as st
from gnani_client import transcribe_bytes, speak_bytes
from scam_rules import check
from messages import MESSAGES
from summary_1930 import build_summary

st.set_page_config(page_title="Ruko", page_icon="🛑")
st.title("🛑 Ruko: रुको, पहले पूछो")
st.caption("A calm voice that warns you about scam calls. Demo with synthetic data only.")

lang_label = st.selectbox("Language / भाषा", ["हिंदी (Hindi)", "मराठी (Marathi)"])
code = "hi-IN" if "Hindi" in lang_label else "mr-IN"

tab1, tab2 = st.tabs(["🎤 Check a call", "🚨 I already sent money"])

with tab1:
    st.write("Press the mic, say what the caller is telling you, then press Stop.")
    recorded = st.audio_input("Record")
    uploaded = st.file_uploader("...or upload a voice note", type=["wav", "ogg", "mp3", "m4a"])
    audio = recorded or uploaded

    if audio is not None and st.button("Check this call"):
        try:
            with st.spinner("Listening..."):
                text = transcribe_bytes(audio.getvalue(), audio.name or "audio.wav", code)
            st.subheader("What I heard")
            st.write(text)

            result = check(text)
            level = result["level"]
            colors = {"HIGH": "red", "MEDIUM": "orange", "LOW": "blue", "NONE": "gray"}
            st.markdown(f"### Risk level: :{colors[level]}[{level}]")
            if result["signals"]:
                st.write("Warning signs found:", ", ".join(result["signals"].keys()))

            message = MESSAGES[code][level]
            st.info(message)

            with st.spinner("Preparing voice..."):
                wav = speak_bytes(message, language=code)
            st.audio(wav, format="audio/wav", autoplay=True)

            st.warning("Ruko cannot prove a call is safe. If anyone asks for money or secrecy, "
                       "stop and call your family or 1930.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")

with tab2:
    st.error("Call **1930** (cyber crime helpline) right now. Do not wait. "
             "Then also report on the official cybercrime portal. Fill this in first so you can read it out.")
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