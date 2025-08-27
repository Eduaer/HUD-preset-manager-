import shutil
import os

def obter_diretorio_jogo():
    with open('myhud/client_config/myhud.txt', 'r', encoding='utf-8') as f:
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
                    raise IndexError("Arquivo de preset ativado não corresponde a nenhuma pasta em 'presets'.")
    raise ValueError("Nenhum preset está ativado.")

def ler_lista_arquivos(caminho_lista):
    with open(caminho_lista, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f if linha.strip()]

def substituir_por_preset(diretorio_jogo, preset_ativo):
    lista_arquivos = ler_lista_arquivos(f'presets/{preset_ativo}/ui_substituir.txt')

    for nome_arquivo in lista_arquivos:
        origem = os.path.join('presets', preset_ativo, 'cinema_hud', 'resource', 'ui', nome_arquivo)
        destino = os.path.join(diretorio_jogo, 'resource', 'ui', nome_arquivo)

        os.makedirs(os.path.dirname(destino), exist_ok=True)

        try:
            shutil.copy2(origem, destino)
            print(f'Substituído: {nome_arquivo}')
        except Exception as e:
            print(f'Erro ao substituir {nome_arquivo}: {e}')

# Execução direta:
if __name__ == '__main__':
    dir_jogo = obter_diretorio_jogo()
    preset_ativo = detectar_preset_ativo()
    substituir_por_preset(dir_jogo, preset_ativo)
