import os
import shutil

def obter_diretorio_jogo():
    with open(os.path.join('myhud', 'client_config', 'myhud.txt'), 'r', encoding='utf-8') as f:
        return f.read().strip()

def restaurar_hudanimations_manifest():
    # Primeiro tenta o caminho original
    origem = os.path.join('myhud', 'client_hud', 'scripts', 'hudanimations_manifest.txt')
    
    # Se não encontrar, usa o arquivo no mesmo diretório do script
    if not os.path.exists(origem):
        print('[INFO] Arquivo de backup não encontrado no caminho original, tentando arquivo local...')
        origem = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hudanimations_manifest.txt')
        
        if not os.path.exists(origem):
            print('[ERRO] Arquivo hudanimations_manifest.txt não encontrado em nenhum local')
            return
        else:
            print('[INFO] Usando arquivo local hudanimations_manifest.txt')
    
    destino_dir = os.path.join(obter_diretorio_jogo(), 'scripts')
    destino = os.path.join(destino_dir, 'hudanimations_manifest.txt')

    os.makedirs(destino_dir, exist_ok=True)

    try:
        shutil.copy2(origem, destino)
        print('[OK] hudanimations_manifest.txt restaurado com sucesso.')
    except Exception as e:
        print(f'[ERRO] Falha ao restaurar hudanimations_manifest.txt: {e}')

if __name__ == '__main__':
    restaurar_hudanimations_manifest()
