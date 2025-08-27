import shutil
import os

def obter_diretorio_jogo():
    with open(os.path.join('myhud', 'client_config', 'myhud.txt'), 'r', encoding='utf-8') as f:
        return f.read().strip()

def obter_preset_ativo():
    preset_base = 'preset_selecionado'
    arquivos = sorted(os.listdir(preset_base))  # 1.txt, 2.txt, etc.
    for i, nome_arquivo in enumerate(arquivos, start=1):
        caminho = os.path.join(preset_base, nome_arquivo)
        with open(caminho, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip().lower()
            if conteudo == 'true':
                pastas_presets = sorted(os.listdir('presets'))
                if i - 1 < len(pastas_presets):
                    return pastas_presets[i - 1]
    return 'default_preset'  # fallback

def ler_lista_arquivos(caminho_lista):
    with open(caminho_lista, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f if linha.strip()]

def restaurar_backup(diretorio_jogo):
    nome_preset = obter_preset_ativo()
    caminho_ui = os.path.join('presets', nome_preset, 'ui_substituir.txt')
    lista_arquivos = ler_lista_arquivos(caminho_ui)

    for nome_arquivo in lista_arquivos:
        # Primeiro tenta restaurar o backup do cliente
        origem = os.path.join('myhud', 'client_hud', 'resource', 'ui', nome_arquivo)
        
        # Se não tiver, usa base do jogo original
        if not os.path.exists(origem):
            origem = os.path.join('base_gamehud', 'resource', 'ui', nome_arquivo)

        destino = os.path.join(diretorio_jogo, 'resource', 'ui', nome_arquivo)

        if os.path.exists(origem):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            try:
                shutil.copy2(origem, destino)
                print(f'[OK] Restaurado: {nome_arquivo}')
            except Exception as e:
                print(f'[ERRO] Ao restaurar {nome_arquivo}: {e}')
        else:
            print(f'[FALHA] Nenhuma fonte encontrada para: {nome_arquivo}')

# Execução direta
if __name__ == '__main__':
    dir_jogo = obter_diretorio_jogo()
    restaurar_backup(dir_jogo)
