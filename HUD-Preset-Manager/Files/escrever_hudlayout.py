import os

def obter_diretorio_jogo():
    with open(os.path.join('myhud', 'client_config', 'myhud.txt'), 'r', encoding='utf-8') as f:
        return f.read().strip()

def detectar_preset_ativo():
    caminho_selecao = 'preset_selecionado'
    if not os.path.exists(caminho_selecao):
        raise FileNotFoundError("Pasta 'preset_selecionado' não encontrada.")

    pastas_presets = sorted(os.listdir('presets'))  # ordem importa
    for i, nome_arquivo in enumerate(sorted(os.listdir(caminho_selecao)), start=0):
        caminho_txt = os.path.join(caminho_selecao, nome_arquivo)
        with open(caminho_txt, 'r', encoding='utf-8') as f:
            if f.read().strip().lower() == 'true':
                if i < len(pastas_presets):
                    return pastas_presets[i]
                else:
                    raise IndexError("Preset ativado não corresponde à pasta em 'presets'.")
    raise ValueError("Nenhum preset está ativado.")

def carregar_valores_modificados(caminho_txt):
    valores = {}  # bloco -> [("chave", "valor"), ...]
    bloco_atual = None

    with open(caminho_txt, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue

            if not linha.startswith('"'):
                bloco_atual = linha
                valores[bloco_atual] = []
            else:
                partes = linha.split('"')
                if len(partes) >= 4:
                    chave = partes[1]
                    valor = partes[3]
                    valores[bloco_atual].append((chave, valor))

    return valores

def carregar_posicoes(caminho_posicoes):
    posicoes = []  # lista de tuplas: (bloco, chave, linha)
    with open(caminho_posicoes, 'r', encoding='utf-8') as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("Bloco:"):
                partes = linha.split('|')
                bloco = partes[0].split(':')[1].strip()
                chave = partes[1].split(':')[1].strip()
                linha_num = int(partes[2].split(':')[1].strip())
                posicoes.append((bloco, chave, linha_num))
    return posicoes

def aplicar_modificacoes(hudlayout_path, posicoes, valores_modificados):
    with open(hudlayout_path, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    for bloco, chave, linha_num in posicoes:
        if bloco in valores_modificados:
            chaves_valores = valores_modificados[bloco]
            for i, (ch, val) in enumerate(chaves_valores):
                if ch == chave:
                    index = linha_num - 1  # Corrige para index 0-based
                    linha_original = linhas[index]
                    prefixo = linha_original.split('"')[0]  # mantém indentação
                    nova_linha = f'{prefixo}"{ch}"\t\t"{val}"\n'
                    linhas[index] = nova_linha
                    print(f'[OK] Linha {linha_num} modificada: {ch} = {val}')
                    valores_modificados[bloco][i] = ("", "")  # marca como usado
                    break

    with open(hudlayout_path, 'w', encoding='utf-8') as f:
        f.writelines(linhas)

# -------------------------
# Execução principal
# -------------------------
if __name__ == '__main__':
    dir_jogo = obter_diretorio_jogo()
    preset = detectar_preset_ativo()
    hudlayout_path = os.path.join(dir_jogo, 'scripts', 'hudlayout.res')

    posicoes_path = 'pos_cl_hud/pos_cl_hud.txt'
    modificacoes_path = f'presets/{preset}/oque_modificar_hudlayout.txt'

    posicoes = carregar_posicoes(posicoes_path)
    valores_mod = carregar_valores_modificados(modificacoes_path)

    aplicar_modificacoes(hudlayout_path, posicoes, valores_mod)
