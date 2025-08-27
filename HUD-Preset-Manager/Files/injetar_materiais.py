import shutil
import os

def obter_diretorio_jogo():
    caminho = os.path.join('myhud', 'client_config', 'myhud.txt')
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read().strip()

def copiar_materiais_para_jogo():
    origem = os.path.join('materials')
    destino = os.path.join(obter_diretorio_jogo(), 'materials')

    if not os.path.exists(origem):
        print('[ERRO] Pasta de materiais da Cinema HUD não encontrada:', origem)
        return

    arquivos_copiados = 0

    for raiz, pastas, arquivos in os.walk(origem):
        for arquivo in arquivos:
            caminho_origem = os.path.join(raiz, arquivo)
            rel_path = os.path.relpath(caminho_origem, origem)
            caminho_destino = os.path.join(destino, rel_path)

            os.makedirs(os.path.dirname(caminho_destino), exist_ok=True)

            try:
                shutil.copy2(caminho_origem, caminho_destino)
                arquivos_copiados += 1
            except Exception as e:
                print(f'[ERRO] Falha ao copiar {rel_path}: {e}')

    print(f'[OK] {arquivos_copiados} arquivos de materiais foram copiados com sucesso para o jogo.')

# Execução
if __name__ == '__main__':
    copiar_materiais_para_jogo()
