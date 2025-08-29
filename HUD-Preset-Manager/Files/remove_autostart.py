import os
from pathlib import Path

def remover_atalho_do_startup(nome_atalho: str = "cinhud_toggle.exe.lnk"):
    """
    Remove o atalho especificado da pasta Startup do Windows
    """
    try:
        # Pasta Startup do usuário atual
        startup_dir = Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        
        # Caminho completo do atalho dentro da pasta Startup
        atalho_path = startup_dir / nome_atalho
        
        # Verificar se o atalho existe
        if atalho_path.exists():
            # Remover o atalho
            atalho_path.unlink()
            print(f"[OK] Atalho removido com sucesso: {atalho_path}")
            print(f"[SUCESSO] Auto start desabilitado!")
        else:
            print(f"[INFO] Atalho nao encontrado: {atalho_path}")
            print(f"[INFO] Auto start ja estava desabilitado!")
            
    except Exception as e:
        print(f"[ERRO] Erro ao remover atalho: {e}")

if __name__ == "__main__":
    remover_atalho_do_startup()
