import subprocess
import os

# 1. Orodha ya maktaba tulizotumia
requirements = """streamlit
psutil
pyautogui
Pillow
"""

file_name = "requirements.txt"

# 2. Tengeneza na andika faili hilo
with open(file_name, "w") as f:
    f.write(requirements)

print(f"Faili la {file_name} limetengenezwa!")

# 3. Fungua Notepad kuonyesha faili hilo (Kwa Windows pekee)
try:
    # Hii amri inafungua Notepad na faili letu
    subprocess.Popen(['notepad.exe', file_name])
    print("Notepad imefunguliwa.")
except Exception as e:
    print(f"Imeshindwa kufungua Notepad: {e}")