import os
import shutil

# Caminhos fixos da config
CONFIG_DIR = os.path.join("myhud", "client_config")
TEM_BASE_FILE = os.path.join(CONFIG_DIR, "tem_base_no_hudlayout.txt")
MYHUD_FILE = os.path.join(CONFIG_DIR, "myhud.txt")

def main():
    # 1. Verifica o conteúdo do tem_base_no_hudlayout.txt
    if not os.path.exists(TEM_BASE_FILE):
        print(f"Arquivo não encontrado: {TEM_BASE_FILE}")
        return
    
    with open(TEM_BASE_FILE, "r", encoding="utf-8") as f:
        conteudo = f.read().strip().lower()
    
    if conteudo != "nao":
        print("Nada a fazer, pois o conteúdo não é 'nao'.")
        return

    # 2. Lê o caminho salvo em myhud.txt
    if not os.path.exists(MYHUD_FILE):
        print(f"Arquivo não encontrado: {MYHUD_FILE}")
        return
    
    with open(MYHUD_FILE, "r", encoding="utf-8") as f:
        caminho_hud = f.read().strip()

    if not os.path.exists(caminho_hud):
        print(f"Caminho inválido em myhud.txt: {caminho_hud}")
        return

    # 3. Acessa a pasta scripts e encontra o hudlayout.res
    scripts_dir = os.path.join(caminho_hud, "scripts")
    hudlayout_res = os.path.join(scripts_dir, "hudlayout.res")

    if not os.path.exists(hudlayout_res):
        print(f"hudlayout.res não encontrado em: {scripts_dir}")
        return

    # 4. Cria pasta hudlayoutfolder (se não existir)
    hudlayout_folder = os.path.join(scripts_dir, "hudlayoutfolder")
    os.makedirs(hudlayout_folder, exist_ok=True)

    # 5. Copia o arquivo e renomeia
    destino = os.path.join(hudlayout_folder, "myhudlayout.res")
    shutil.copy2(hudlayout_res, destino)

    print(f"Arquivo copiado para: {destino}")

if __name__ == "__main__":
    main()
