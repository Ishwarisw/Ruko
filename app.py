# app.py - Ruko screen: speak -> check -> spoken warning
import streamlit as st
from gnani_client import transcribe_bytes, speak_bytes
from scam_rules import check
from messages import MESSAGES

st.set_page_config(page_title="Ruko", page_icon="🛑")
st.title("🛑 Ruko: रुको, पहले पूछो")
st.caption("A calm voice that warns you about scam calls. Demo with synthetic data only.")

lang_label = st.selectbox("Language / भाषा", ["हिंदी (Hindi)", "मराठी (Marathi)"])
code = "hi-IN" if "Hindi" in lang_label else "mr-IN"

st.write("Press the mic, say what the caller is telling you, then press Stop.")
recorded = st.audio_input("Record")
uploaded = st.file_uploader("...or upload a voice note (wav, ogg, mp3)", type=["wav", "ogg", "mp3", "m4a"])

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