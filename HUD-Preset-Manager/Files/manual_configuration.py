import tkinter as tk
import subprocess
import os

# Caminho para o Python customizado
python_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-capado", "python.exe")

# Função para rodar scripts Python
def run_py(script_name):
    try:
        subprocess.Popen([python_exe, script_name], shell=True)
    except Exception as e:
        print(f"Erro ao rodar {script_name}: {e}")

# Função para rodar comandos diretos
def run_cmd(cmd):
    try:
        subprocess.Popen(cmd, shell=True)
    except Exception as e:
        print(f"Erro ao rodar comando {cmd}: {e}")

# Criar janela
root = tk.Tk()
root.title("manual configs Control Panel")
root.geometry("300x400")

# Texto de aviso
warning_label = tk.Label(
    root,
    text="Warning: If you disable auto start,\nyou will need to enable the shortcut\nmanually every time you open TF2. \nThe program consumes 0.01 of the CPU \n and 1 MB of RAM.",
    fg="black",
    font=("Arial", 9, "bold"),
    justify="center"
)
warning_label.pack(pady=10)

# Botões
btn1 = tk.Button(root, text="Disable Start with Windows", width=30,
                 command=lambda: [run_py("remove_autostart.py"), run_py("disableautostart.py")])
btn1.pack(pady=2)

btn2 = tk.Button(root, text="Enable Start with Windows", width=30,
                 command=lambda: [run_py("ableautostart.py"), run_py("disbleautostart/create_shortcut_auto_start.py")])
btn2.pack(pady=2)

btn3 = tk.Button(root, text="Stop Shortcut", width=30,
                 command=lambda: run_cmd("taskkill /f /im cinhud_toggle.exe"))
btn3.pack(pady=2)

btn4 = tk.Button(root, text="Enable Shortcut", width=30,
                 command=lambda: run_cmd(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cinhud_toggle.exe")))
btn4.pack(pady=2)

btn5 = tk.Button(root, text="Add preset to game", width=30,
                 command=lambda: run_py("addtogame.py"))
btn5.pack(pady=2)

btn6 = tk.Button(root, text="come back to my hud", width=30,
                 command=lambda: run_py("revert.py"))
btn6.pack(pady=2)

# Rodar loop
root.mainloop()
