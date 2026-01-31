import streamlit as st
import os
import psutil
import time
import speech_recognition as sr
from gtts import gTTS
from streamlit_mic_recorder import mic_recorder
import io
import pyautogui

# Mipangilio ya Dashboard
st.set_page_config(page_title="Megatron Voice Command", page_icon="🤖")

# --- Kazi ya Megatron Kuzungumza (Sauti ya Robot) ---
def megatron_speak(text):
    tts = gTTS(text=text, lang='en') 
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    st.audio(audio_fp, format='audio/mp3', autoplay=True)

# --- Session State ya Kumbukumbu ---
if "status" not in st.session_state:
    st.session_state.status = "SLEEPING"
if "pending_command" not in st.session_state:
    st.session_state.pending_command = None

# --- UI YA FRONT-END ---
st.markdown("<h1 style='text-align: center; color: red;'>MEGATRON INTELLIGENCE OS</h1>", unsafe_allow_html=True)

# Pakia Picha ya Robot (Megatron.png)
if os.path.exists("megatron.png"):
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("megatron.png", caption="Megatron is watching you...")
else:
    st.warning("Picha ya 'megatron.png' haipo kwenye folder hili!")

st.divider()

# Hali ya sasa
st.subheader(f"Hali ya Megatron: `{st.session_state.status}`")

# --- KUREKODI SAUTI ---
st.write("Bonyeza mic, zungumza, kisha subiri Megatron ajibu:")
audio = mic_recorder(start_prompt="🎤 ZUNGUMZA NA MEGATRON", stop_prompt="🛑 ACHA", key='recorder')

if audio:
    r = sr.Recognizer()
    audio_data = sr.AudioData(audio['bytes'], 16000, 2)
    try:
        # Geuza sauti kuwa maandishi (Inatumia Google Speech API)
        command = r.recognize_google(audio_data).lower()
        st.write(f"💬 **Umesema:** {command}")

        # --- LOGIC ZA MEGATRON ---

        # 1. Kuanza: Megatron lazima aitwe
        if st.session_state.status == "SLEEPING":
            if "megatron" in command:
                st.session_state.status = "LISTENING"
                megatron_speak("AS YOU COMMAND")
                st.rerun()
            else:
                st.warning("Megatron hasikilizi... Anza kwa kusema jina lake.")

        # 2. Kupokea Amri (Zima/Washa)
        elif st.session_state.status == "LISTENING":
            if "zima pc" in command or "shutdown" in command:
                st.session_state.pending_command = "ZIMA PC"
                st.session_state.status = "CONFIRMING"
                megatron_speak(f"{st.session_state.pending_command} command confirmed. Confirm with GO or ACHA")
            elif "washa pc" in command or "restart" in command:
                st.session_state.pending_command = "WASHA PC"
                st.session_state.status = "CONFIRMING"
                megatron_speak(f"{st.session_state.pending_command} command confirmed. Confirm with GO or ACHA")
            elif "acha" in command or "stop" in command:
                st.session_state.status = "SLEEPING"
                megatron_speak("ACHA! I am ignoring your request.")
            st.rerun()

        # 3. Hatua ya Mwisho (GO au ACHA)
        elif st.session_state.status == "CONFIRMING":
            if "go" in command:
                megatron_speak("EXECUTING NOW. GOODBYE.")
                time.sleep(2)
                if st.session_state.pending_command == "ZIMA PC":
                    os.system("shutdown /s /t 1")
                elif st.session_state.pending_command == "WASHA PC":
                    os.system("shutdown /r /t 1")
            elif "acha" in command:
                st.session_state.status = "SLEEPING"
                st.session_state.pending_command = None
                megatron_speak("ACHA! Process terminated.")
                st.rerun()

    except Exception as e:
        st.error("Megatron ameshindwa kukuelewa. Zungumza waziwazi!")

# System Stats Sidebar
st.sidebar.header("Megatron Sensors")
st.sidebar.progress(psutil.cpu_percent() / 100, text="CPU Usage")
st.sidebar.progress(psutil.virtual_memory().percent / 100, text="RAM Usage")
