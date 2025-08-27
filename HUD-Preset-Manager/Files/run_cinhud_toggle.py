import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
txt_path = os.path.join(BASE_DIR, "install_fisrt_time.txt")
ahk_script = os.path.join(BASE_DIR, "cinhud_toggle.exe")  # ou .ahk

if os.path.exists(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        valor = f.read().strip()
        if valor == "0":
            try:
                subprocess.run(ahk_script, shell=True, check=True)
            except subprocess.CalledProcessError:
                pass  # ignora erro se quiser
# Finaliza imediatamente
sys.exit(0)
