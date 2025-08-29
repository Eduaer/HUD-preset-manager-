import os
from pathlib import Path
import win32com.client  # requer pywin32

def criar_atalho_no_startup(arquivo_ahk: str, nome_atalho: str = "cinhud_toggle.exe.lnk"):
    # Caminho do script .ahk (pode ser relativo ou absoluto)
    arquivo_ahk = Path(arquivo_ahk).resolve()

    # Pasta Startup do usuário atual
    startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"

    # Caminho completo do atalho dentro da pasta Startup
    atalho_path = startup_dir / nome_atalho

    # Criar o atalho com pywin32
    shell = win32com.client.Dispatch("WScript.Shell")
    atalho = shell.CreateShortcut(str(atalho_path))
    atalho.TargetPath = str(arquivo_ahk)
    atalho.WorkingDirectory = str(arquivo_ahk.parent)
    atalho.Save()

    print(f"Atalho criado em: {atalho_path}")

if __name__ == "__main__":
    criar_atalho_no_startup("cinhud_toggle.exe")
