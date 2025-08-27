import shutil
import os

def obter_diretorio_jogo():
    caminho = os.path.join('myhud', 'client_config', 'myhud.txt')
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read().strip()

def restaurar_hudlayout():
    origem = os.path.join('myhud', 'client_hud', 'scripts', 'hudlayout.res')
    destino_dir = os.path.join(obter_diretorio_jogo(), 'scripts')
    destino = os.path.join(destino_dir, 'hudlayout.res')

    if not os.path.exists(origem):
        print('[ERRO] Arquivo de HUD original não encontrado:', origem)
        return

    os.makedirs(destino_dir, exist_ok=True)

    try:
        shutil.copy2(origem, destino)
        print('[OK] hudlayout.res restaurado para o diretório do jogo.')
    except Exception as e:
        print(f'[ERRO] Falha ao restaurar hudlayout.res: {e}')

# Execução
if __name__ == '__main__':
    restaurar_hudlayout()
