import streamlit as st
import os
import psutil
import pyautogui
import io
import time
import platform
import gc
from PIL import Image

# 1. MIPANGILIO YA DASHBOARD
st.set_page_config(page_title="Megatron Command Center", layout="wide")

# NENOSIRI
SECRET_PASSWORD = "transformers2026"

# 2. ULINZI (LOGIN)
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Mfumo Umefungwa")
    pwd = st.text_input("Ingiza Nenosiri la Megatron:", type="password")
    if st.button("Fungua"):
        if pwd == SECRET_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Nenosiri si sahihi!")
    st.stop()

# 3. NAVIGATION STATE KWA FILE EXPLORER
if "current_path" not in st.session_state:
    st.session_state["current_path"] = os.path.expanduser("~") # Anza kwenye folder la User

# --- SIDEBAR: SYSTEM STATUS ---
st.sidebar.title("🤖 System Monitor")
with st.sidebar:
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_data = psutil.virtual_memory()
    st.metric("CPU", f"{cpu_usage}%")
    st.metric("RAM", f"{ram_data.percent}%")
    
    st.divider()
    if st.button("🛑 ZIMA PC"):
        os.system("shutdown /s /t 10")
        st.warning("PC itazima baada ya sekunde 10!")
    if st.button("🔄 RESTART"):
        os.system("shutdown /r /t 10")
        st.info("PC itawaka upya...")

# --- MAIN INTERFACE ---
tab1, tab2 = st.tabs(["📺 Live Stream (Optimized)", "📂 Advanced File Explorer"])

# --- TAB 1: LIVE STREAM (Anti-MemoryError Logic) ---
with tab1:
    st.header("Live View (Low Latency)")
    streaming = st.toggle("Washa Stream")
    placeholder = st.empty()
    
    if streaming:
        st.toast("Inarusha picha...")
        while streaming:
            try:
                # Piga picha ya kioo
                screenshot = pyautogui.screenshot()
                
                # 1. Optimization: Punguza ukubwa (Hii inazuia MemoryError)
                # 640x360 ni bora kwa simu na inatumia RAM kidogo sana
                screenshot = screenshot.resize((640, 360))
                
                # 2. Optimization: Tumia JPEG na Quality ya 50
                buf = io.BytesIO()
                screenshot.save(buf, format='JPEG', quality=50, optimize=True)
                
                placeholder.image(buf.getvalue(), use_container_width=True)
                
                # 3. Optimization: Safisha Memory
                del screenshot
                buf.close()
                gc.collect() # Lazimisha Python kusafisha RAM iliyobaki
                
                time.sleep(0.05) # Speed control
            except Exception as e:
                st.error(f"Hitilafu ya Stream: {e}")
                break
    else:
        placeholder.info("Washa toggle hapo juu kuanza kuona kioo cha PC.")

# --- TAB 2: ADVANCED FILE EXPLORER ---
with tab2:
    st.header("File Navigator")
    
    # Path ya sasa na kitufe cha kurudi nyuma
    curr_path = st.session_state["current_path"]
    col_path, col_back = st.columns([4, 1])
    
    col_path.code(f"Folder: {curr_path}")
    if col_back.button("⬅️ Rudi Nyuma"):
        st.session_state["current_path"] = os.path.dirname(curr_path)
        st.rerun()

    try:
        # Pata list ya mafaili
        items = os.listdir(curr_path)
        items.sort(key=lambda x: os.path.isdir(os.path.join(curr_path, x)), reverse=True)

        for item in items:
            item_path = os.path.join(curr_path, item)
            is_dir = os.path.isdir(item_path)
            
            c1, c2 = st.columns([0.8, 0.2])
            
            if is_dir:
                if c1.button(f"📁 {item}", key=item_path, use_container_width=True):
                    st.session_state["current_path"] = item_path
                    st.rerun()
            else:
                c1.write(f"📄 {item}")
                # Download button (Ili kuzuia MemoryError, usipakue faili > 50MB)
                file_size = os.path.getsize(item_path) / (1024 * 1024)
                if file_size < 50:
                    with open(item_path, "rb") as f:
                        c2.download_button("Pakua", f, file_name=item, key=f"dl_{item_path}")
                else:
                    c2.write("🐘 Too Big")
                    
    except PermissionError:
        st.error("Huna ruhusa ya kufungua folder hili!")
    except Exception as e:
        st.error(f"Hitilafu: {e}")