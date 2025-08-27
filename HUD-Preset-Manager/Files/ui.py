import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# =============================
# CONFIGURAÇÕES
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CUSTOM_PRESETS_DIR = os.path.join(BASE_DIR, "custom presets")
BACKUP_DIR = os.path.join(BASE_DIR, "backup cinhud")
MAX_PRESETS = 20

# Caminho para o python.exe específico
python_exe = os.path.join(BASE_DIR, "python-capado", "python.exe")

subprocess.Popen(
    [python_exe, os.path.join(BASE_DIR, "run_cinhud_toggle.py")],
    shell=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Nome do arquivo de verificação
INSTALL_FIRST_TIME_PATH = os.path.join(BASE_DIR, "install_fisrt_time.txt")  # padronizado com o segundo código

# =============================
# VARIÁVEIS GLOBAIS
# =============================
preset_atual = 0
main_frame = None

# =============================
# FUNÇÕES AUXILIARES
# =============================
def get_preset_path(num):
    """Retorna o caminho para a pasta default_preset do preset dado."""
    if num == 0:
        return os.path.join(BACKUP_DIR, "default_preset")
    else:
        return os.path.join(CUSTOM_PRESETS_DIR, str(num), "default_preset")

def carregar_preset(num):
    """Atualiza a tela com o preset selecionado."""
    global preset_atual
    preset_path = get_preset_path(num)

    for widget in main_frame.winfo_children():
        widget.destroy()

    if not os.path.exists(preset_path):
        tk.Label(main_frame, text="Oh no, you've run out of available presets.",
                 font=("Arial", 14)).pack(pady=20)
        tk.Label(main_frame, text="Click the button below to learn how to create a preset.",
                 font=("Arial", 12)).pack(pady=5)
        tk.Button(main_frame, text="Click me", command=abrir_janela_como_criar).pack(pady=10)
        tk.Button(main_frame, text="Previous", command=lambda: carregar_preset(preset_atual - 1)).pack(pady=5)
        return

    preset_atual = num

    # Ler título
    title_file = os.path.join(preset_path, "title.txt")
    title = open(title_file, "r", encoding="utf-8").read().strip() if os.path.exists(title_file) else "No title"

    # Ler descrição
    desc_file = os.path.join(preset_path, "description.txt")
    desc = open(desc_file, "r", encoding="utf-8").read().strip() if os.path.exists(desc_file) else "No description"

    # Ler imagem
    img_file = os.path.join(preset_path, "img.png")
    img = tk.PhotoImage(file=img_file) if os.path.exists(img_file) else None

    # Exibir título
    tk.Label(main_frame, text=title, font=("Arial", 16, "bold")).pack(pady=5)

    # Exibir imagem
    if img:
        lbl_img = tk.Label(main_frame, image=img)
        lbl_img.image = img
        lbl_img.pack()

    # Exibir descrição
    tk.Label(main_frame, text=desc, wraplength=500, justify="left").pack(pady=5)

    # Botões next/previous
    nav_frame = tk.Frame(main_frame)
    nav_frame.pack(pady=10)
    btn_prev = tk.Button(nav_frame, text="Previous", command=lambda: carregar_preset(num - 1))
    btn_prev.grid(row=0, column=0, padx=5)
    if num == 0:
        btn_prev.config(state="disabled")

    btn_next = tk.Button(nav_frame, text="Next", command=lambda: carregar_preset(num + 1))
    btn_next.grid(row=0, column=1, padx=5)

    # Botão Select Preset
    tk.Button(main_frame, text="Select Preset",
              command=lambda: selecionar_preset(num)).pack(pady=5)

    # Botão Install
    tk.Button(main_frame, text="Install",
              command=lambda: instalar_preset(num)).pack(pady=5)

def is_first_time_install():
    """Verifica se é a primeira instalação."""
    if os.path.exists(INSTALL_FIRST_TIME_PATH):
        try:
            with open(INSTALL_FIRST_TIME_PATH, "r") as f:
                value = f.read().strip()
            return value == "1"
        except:
            return False
    return False
    
def selecionar_preset(num):
    """Chama o script de troca de preset e injeta materiais."""
    # Executar change_presets.py
    subprocess.run([python_exe, os.path.join(BASE_DIR, "change_presets.py"), str(num)], shell=True)
    
    # Executar injetar_materiais.py
    subprocess.run([python_exe, os.path.join(BASE_DIR, "injetar_materiais.py")], shell=True)


    
    # Mostrar mensagem de confirmação
    messagebox.showinfo("                ","          ok")

def instalar_preset(num):
    """Fluxo do botão Install com verificação integrada."""
    # Passo 1: Mostrar mensagem "select your hud folder..."
    messagebox.showinfo("Select HUD Folder",
                        "select your hud folder example:\nC:\\SteamLibrary\\steamapps\\common\\Team Fortress 2\\tf\\custom\\budhud")
    

    


    # Passo 3: Verificar se é a primeira instalação
    if is_first_time_install():
        resp = messagebox.askokcancel("warning",
                                      "You just need to click the install button when you change your TF2 HUD.\n"
                                      "If you want to change the preset, press 'select preset'")
        if not resp:
            return

    # Passo 4: Rodar install.py
    result = subprocess.run([python_exe, os.path.join(BASE_DIR, "install.py")],
                            shell=True, capture_output=True, text=True)
    if "[ERRO]" in result.stdout:
        messagebox.showerror("Error", "The preset is installed now.\nRevert to your original HUD before installing again.")
    else:
        # Passo 5: Se a instalação foi bem-sucedida, executar install_first_time_check.py
        subprocess.run([python_exe, os.path.join(BASE_DIR, "install_first_time_check.py")], shell=True)

def abrir_janela_como_criar():
    """Abre uma nova janela para o texto 'como criar preset'."""
    win = tk.Toplevel()
    win.title("How to Create a Preset")
    
    # Ler o conteúdo do arquivo guide.txt
    try:
        with open("guide.txt", "r", encoding="utf-8") as f:
            guide_text = f.read()
    except FileNotFoundError:
        guide_text = "Arquivo guide.txt não encontrado."
    except Exception as e:
        guide_text = f"Erro ao ler o arquivo: {str(e)}"
    
    tk.Label(win, text=guide_text, wraplength=400).pack(padx=10, pady=10)

# =============================
# INTERFACE PRINCIPAL
# =============================
root = tk.Tk()
root.title("HUD Preset Manager")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Aba Main
main_frame = tk.Frame(notebook)
notebook.add(main_frame, text="Main")

# Aba Install Guide
install_guide_frame = tk.Frame(notebook)
notebook.add(install_guide_frame, text="Install Guide")

# Ler o conteúdo do arquivo install_guide.txt
try:
    with open("install_guide.txt", "r", encoding="utf-8") as f:
        install_guide_text = f.read()
except FileNotFoundError:
    install_guide_text = "Arquivo install_guide.txt não encontrado."
except Exception as e:
    install_guide_text = f"Erro ao ler o arquivo: {str(e)}"

# Criar um widget Text para permitir seleção e cópia do texto
text_widget = tk.Text(install_guide_frame, wrap="word", width=60, height=20, 
                     font=("Arial", 10), padx=10, pady=10)
text_widget.pack(padx=10, pady=10, fill="both", expand=True)

# Inserir o texto no widget
text_widget.insert("1.0", install_guide_text)

# Configurar o widget como somente leitura (não editável)
text_widget.config(state="disabled")

# Aba More Details
more_details_frame = tk.Frame(notebook)
notebook.add(more_details_frame, text="More Details")


tk.Label(more_details_frame, text="Thanks for downloading.", 
         font=("Arial", 12, "bold"), justify="left", fg="black").pack(pady=5)



explicacao_texto = """The way the code works is extremely simple. 
It basically moves, deletes, and edits text files in the right order using Python, and then uses AutoHotkey to trigger the scripts with the keys."""

tk.Label(more_details_frame, text=explicacao_texto, 
         wraplength=500, justify="left", font=("Arial", 10)).pack(pady=10)

# Carregar e exibir a imagem
try:
    img_path = os.path.join(BASE_DIR, "Sem Título-1.png")
    if os.path.exists(img_path):
        img_more = tk.PhotoImage(file=img_path)
        lbl_img_more = tk.Label(more_details_frame, image=img_more)
        lbl_img_more.image = img_more  # Manter referência
        lbl_img_more.pack(pady=10)
    else:
        tk.Label(more_details_frame, text="Imagem 'Sem Título-1.png' não encontrada",
                 fg="red").pack(pady=10)
except Exception as e:
    tk.Label(more_details_frame, text=f"Erro ao carregar imagem: {str(e)}",
             fg="red").pack(pady=10)

# Botão aiiiiiiiiiiii
def executar_audio():
    """Executa o arquivo playaudiofilefromUI.py"""
    subprocess.run([python_exe, os.path.join(BASE_DIR, "playaudiofilefromUI.py")], shell=True)
btn_ai = tk.Button(
    more_details_frame,
    text="aiiiiiiiiiii",
    command=executar_audio,
    font=("Arial", 10, "bold"),
    width=18,
    height=2
)
btn_ai.pack(pady=10)

# Função para abrir o link do Steam
def abrir_link_steam():
    import webbrowser
    webbrowser.open("http://steamcommunity.com/tradeoffer/new/?partner=1264933955&token=q2fueoJA")

# Frase e link clicável
tk.Label(more_details_frame, text="give me tf2 items:", 
         font=("Arial", 10, "bold"), justify="left").pack(pady=2)

link_steam = tk.Label(more_details_frame, text="http://steamcommunity.com/tradeoffer/new/?partner=1264933955&token=q2fueoJA", 
                      font=("Arial", 10), fg="blue", cursor="hand2")
link_steam.pack(pady=2)
link_steam.bind("<Button-1>", lambda e: abrir_link_steam())
link_steam.bind("<Enter>", lambda e: link_steam.config(fg="red"))
link_steam.bind("<Leave>", lambda e: link_steam.config(fg="blue"))



# Carregar primeiro preset
carregar_preset(0)

root.mainloop()