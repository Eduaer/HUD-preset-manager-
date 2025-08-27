import os
import shutil

def obter_diretorio_jogo():
    with open(os.path.join('myhud', 'client_config', 'myhud.txt'), 'r', encoding='utf-8') as f:
        return f.read().strip()

def detectar_preset_ativo():
    caminho_selecao = 'preset_selecionado'
    if not os.path.exists(caminho_selecao):
        raise FileNotFoundError("Pasta 'preset_selecionado' não encontrada.")

    pastas_presets = sorted(os.listdir('presets'))
    for i, nome_arquivo in enumerate(sorted(os.listdir(caminho_selecao)), start=0):
        caminho_txt = os.path.join(caminho_selecao, nome_arquivo)
        with open(caminho_txt, 'r', encoding='utf-8') as f:
            if f.read().strip().lower() == 'true':
                if i < len(pastas_presets):
                    return pastas_presets[i]
                else:
                    raise IndexError("Preset ativado não corresponde à pasta em 'presets'.")
    raise ValueError("Nenhum preset está ativado.")

def injetar_hudlayout_base(diretorio_jogo, preset):
    nome_pasta_injetada = f"hudlayout_ad_in_{preset}"
    
    origem_hudlayout = os.path.join('presets', preset, 'hudlayout_ad_in', 'scripts', 'hudlayout.res')
    destino_pasta = os.path.join(diretorio_jogo, nome_pasta_injetada, 'scripts')
    destino_hudlayout = os.path.join(destino_pasta, 'hudlayout.res')

    if not os.path.exists(origem_hudlayout):
        print(f'[AVISO] Arquivo não encontrado para injetar: {origem_hudlayout}')
        return

    os.makedirs(destino_pasta, exist_ok=True)
    shutil.copy2(origem_hudlayout, destino_hudlayout)
    print(f'[OK] Arquivo de override copiado para: {destino_hudlayout}')

    # Agora injeta o #base no hudlayout do cliente
    hudlayout_cliente = os.path.join(diretorio_jogo, 'scripts', 'hudlayout.res')

    if not os.path.exists(hudlayout_cliente):
        print('[ERRO] hudlayout.res do cliente não encontrado.')
        return

    with open(hudlayout_cliente, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    base_override = f'#base   "../{nome_pasta_injetada}/scripts/hudlayout.res"\n'

    if base_override not in linhas:
        linhas.insert(0, '\n')
        linhas.insert(0, base_override)
        with open(hudlayout_cliente, 'w', encoding='utf-8') as f:
            f.writelines(linhas)
        print('[OK] #base override adicionado no topo do hudlayout.res do cliente.')
    else:
        print('[INFO] #base já presente no hudlayout.res do cliente.')

# Execução direta
if __name__ == '__main__':
    dir_jogo = obter_diretorio_jogo()
    preset = detectar_preset_ativo()
    injetar_hudlayout_base(dir_jogo, preset)
