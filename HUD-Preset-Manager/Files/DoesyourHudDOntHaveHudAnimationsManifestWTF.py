import os
import shutil

# Caminho base (onde está o script e o myhud.txt)

CAMINHO_BASE = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MYHUD_TXT = os.path.join(CAMINHO_BASE, 'myhud', 'client_config', "myhud.txt")

def main():
    # Lê o caminho salvo no myhud.txt
    if not os.path.exists(CAMINHO_MYHUD_TXT):
        print("Erro: myhud.txt não encontrado.")
        return
    
    with open(CAMINHO_MYHUD_TXT, "r", encoding="utf-8") as f:
        caminho_hud = f.read().strip()

    if not os.path.exists(caminho_hud):
        print("Erro: caminho da HUD no myhud.txt é inválido.")
        return

    # Caminho da pasta scripts da HUD
    pasta_scripts = os.path.join(caminho_hud, "scripts")

    if not os.path.exists(pasta_scripts):
        print("Erro: a pasta 'scripts' não existe dentro da HUD.")
        return

    # Caminho do arquivo dentro da HUD
    arquivo_destino = os.path.join(pasta_scripts, "hudanimations_manifest.txt")

    # Caminho do arquivo local (mesmo diretório do script)
    arquivo_origem = os.path.join(CAMINHO_BASE, "hudanimations_manifest.txt")

    # Se já existe, não faz nada
    if os.path.exists(arquivo_destino):
        print("O arquivo 'hudanimations_manifest.txt' já existe dentro da HUD.")
        return

    # Se não existe, copia
    if not os.path.exists(arquivo_origem):
        print("Erro: arquivo 'hudanimations_manifest.txt' não encontrado no diretório do script.")
        return

    shutil.copy2(arquivo_origem, arquivo_destino)
    print("Arquivo 'hudanimations_manifest.txt' copiado com sucesso para a pasta scripts da HUD.")

if __name__ == "__main__":
    main()
