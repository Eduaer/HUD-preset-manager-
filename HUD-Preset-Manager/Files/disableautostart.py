import os
import shutil
from pathlib import Path

def copiar_arquivo():
    # Obter o diretório atual onde está este script
    current_dir = Path(__file__).parent
    
    # Caminhos dos arquivos e pastas
    arquivo_principal = current_dir / "create_shortcut_auto_start.py"
    arquivo_fakeautostart = current_dir / "fakeautostart" / "create_shortcut_auto_start.py"
    
    try:
        # Verificar se o arquivo de origem existe
        if not arquivo_fakeautostart.exists():
            print("[ERRO] Arquivo da pasta fakeautostart nao encontrado")
            return
        
        # 1. Excluir o arquivo create_shortcut_auto_start.py da pasta principal se existir
        if arquivo_principal.exists():
            os.remove(arquivo_principal)
            print(f"[OK] Arquivo existente removido: {arquivo_principal}")
        
        # 2. Copiar o arquivo da pasta fakeautostart para a pasta principal
        shutil.copy2(str(arquivo_fakeautostart), str(arquivo_principal))
        print(f"[OK] Arquivo copiado para: {arquivo_principal}")
        
        # 3. Verificar se a cópia foi bem-sucedida
        if arquivo_principal.exists():
            print("\n[SUCESSO] Copia concluida com sucesso!")
        else:
            print("\n[ERRO] Falha na copia - arquivo nao foi criado")
            
    except Exception as e:
        print(f"[ERRO] Erro durante a copia: {e}")

if __name__ == "__main__":
    copiar_arquivo()




