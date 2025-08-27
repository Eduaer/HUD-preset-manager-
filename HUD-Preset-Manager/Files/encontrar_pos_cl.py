import os

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

def carregar_blocos(nome_arquivo_blocos):
    with open(nome_arquivo_blocos, 'r', encoding='utf-8') as f:
        blocos = [linha.strip() for linha in f if linha.strip()]
    return blocos

def encontrar_linhas_chave_em_blocos(nome_arquivo_res, blocos, chaves_procuradas):
    with open(nome_arquivo_res, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    resultados = []
    total_linhas = len(linhas)
    i = 0

    while i < total_linhas:
        linha = linhas[i].strip()

        for bloco in blocos:
            if linha.startswith(bloco):
                while i < total_linhas and "{" not in linhas[i]:
                    i += 1
                i += 1

                nivel = 1
                while i < total_linhas and nivel > 0:
                    linha_atual = linhas[i].strip()

                    if "{" in linha_atual:
                        nivel += 1
                    if "}" in linha_atual:
                        nivel -= 1

                    for chave in chaves_procuradas:
                        if chave in linha_atual:
                            resultados.append((bloco, chave, i + 1))
                    i += 1
                break
        else:
            i += 1

    return resultados

def salvar_resultados(nome_saida, resultados):
    with open(nome_saida, 'w', encoding='utf-8') as f:
        for bloco, chave, linha in resultados:
            f.write(f'Bloco: {bloco} | Chave: {chave} | Linha: {linha}\n')

# ---------------------
# Execução principal
# ---------------------
if __name__ == '__main__':
    preset_ativo = detectar_preset_ativo()

    hudlayout_cliente = os.path.join('myhud', 'client_hud', 'scripts', 'hudlayout.res')
    saida_resultados = os.path.join('pos_cl_hud', 'pos_cl_hud.txt')
    caminho_blocos = os.path.join('presets', preset_ativo, 'blocos_hudlayout.txt')

    blocos = carregar_blocos(caminho_blocos)
    chaves = ['xpos', 'ypos', 'xpos_minmode', 'ypos_minmode', 'wide', 'tall']

    resultados = encontrar_linhas_chave_em_blocos(hudlayout_cliente, blocos, chaves)
    salvar_resultados(saida_resultados, resultados)

    print(f"[OK] Busca concluída. {len(resultados)} posições salvas em '{saida_resultados}'")
