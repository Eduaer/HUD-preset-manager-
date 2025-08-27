import os
import shutil

def obter_diretorio_jogo():
    with open(os.path.join('myhud', 'client_config', 'myhud.txt'), 'r', encoding='utf-8') as f:
        return f.read().strip()

def obter_preset_ativo():
    base_presets = os.path.join('presets')
    selecionado_dir = os.path.join('preset_selecionado')

    pastas_presets = sorted(os.listdir(base_presets))
    txts_selecao = sorted(os.listdir(selecionado_dir))

    for i, txt in enumerate(txts_selecao):
        caminho_txt = os.path.join(selecionado_dir, txt)
        with open(caminho_txt, 'r', encoding='utf-8') as f:
            if f.read().strip().lower() == 'true':
                return pastas_presets[i]
    raise Exception('[ERRO] Nenhum preset marcado como TRUE em preset_selecionado')

def injetar_animations(diretorio_jogo):
    preset = obter_preset_ativo()

    pasta_origem = os.path.join('presets', preset, 'aninmIN', 'scripts')
    pasta_destino = os.path.join(diretorio_jogo, 'scripts')
    hudanimations_manifest = os.path.join(diretorio_jogo, 'scripts', 'hudanimations_manifest.txt')  # CORRIGIDO
    nome_da_pasta_custom = os.path.basename(diretorio_jogo)

    if not os.path.isdir(pasta_origem):
        print(f'[INFO] Pasta de animações não encontrada: {pasta_origem}')
        return

    arquivos_injetados = []

    for nome_arquivo in os.listdir(pasta_origem):
        if nome_arquivo.endswith('.txt'):
            origem = os.path.join(pasta_origem, nome_arquivo)
            destino = os.path.join(pasta_destino, nome_arquivo)

            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copy2(origem, destino)
            arquivos_injetados.append(nome_arquivo)
            print(f'[OK] Injetado: {nome_arquivo} em {destino}')

    if not arquivos_injetados:
        print('[INFO] Nenhum arquivo .txt para injetar.')
        return

    if not os.path.exists(hudanimations_manifest):
        print('[ERRO] hudanimations_manifest.txt não encontrado.')
        return

    with open(hudanimations_manifest, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    for nome_arquivo in arquivos_injetados:
        caminho_relativo = f'scripts/{nome_arquivo}'  # <<--- CORRIGIDO
        linha_injetar = f'\t"file"\t"{caminho_relativo}"\n'

        if linha_injetar not in linhas:
            for i, linha in enumerate(linhas):
                if linha.strip().startswith('{'):
                    linhas.insert(i + 1, linha_injetar)
                    print(f'[OK] Linha adicionada ao manifest: {linha_injetar.strip()}')
                    break

    with open(hudanimations_manifest, 'w', encoding='utf-8') as f:
        f.writelines(linhas)
    print('[OK] hudanimations_manifest.txt atualizado com sucesso.')

if __name__ == '__main__':
    dir_jogo = obter_diretorio_jogo()
    injetar_animations(dir_jogo)
