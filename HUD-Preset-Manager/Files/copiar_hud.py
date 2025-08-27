import shutil
import os

def copiar_hud_para_client(prototipo_destino='myhud\\client_hud'):
    config_arquivo = os.path.join('myhud', 'client_config', 'myhud.txt')

    if not os.path.exists(config_arquivo):
        print("Erro: O arquivo myhud.txt não existe. Execute primeiro salvar_hud.py.")
        return

    with open(config_arquivo, 'r', encoding='utf-8') as f:
        origem = f.read().strip()

    if not origem or not os.path.exists(origem):
        print("Erro: Caminho inválido ou pasta não encontrada.")
        return

    if os.path.exists(prototipo_destino):
        try:
            shutil.rmtree(prototipo_destino)  # Remove a antiga
        except Exception as e:
            print(f"Erro ao limpar client_hud: {e}")
            return

    try:
        shutil.copytree(origem, prototipo_destino)
        print(f"HUD copiada com sucesso para '{prototipo_destino}'.")
    except Exception as e:
        print(f"Erro ao copiar HUD: {e}")

if __name__ == '__main__':
    copiar_hud_para_client()
