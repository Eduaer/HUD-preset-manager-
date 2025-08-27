import os

def obter_diretorio_jogo():
    """Lê o caminho do jogo salvo em myhud/client_config/myhud.txt"""
    caminho_config = os.path.join('myhud', 'client_config', 'myhud.txt')
    if not os.path.exists(caminho_config):
        raise FileNotFoundError(f"[ERRO] Arquivo {caminho_config} não encontrado.")
    
    with open(caminho_config, 'r', encoding='utf-8') as f:
        return f.read().strip()

def detectar_base_em_hudlayout(diretorio_jogo):
    """Procura por '#base' dentro do hudlayout.res do jogo"""
    caminho_hudlayout = os.path.join(diretorio_jogo, 'scripts', 'hudlayout.res')
    resultado = 'nao'

    if os.path.exists(caminho_hudlayout):
        with open(caminho_hudlayout, 'r', encoding='utf-8', errors='ignore') as f:
            for linha in f:
                if '#base' in linha.lower():  # deixa case-insensitive
                    resultado = 'sim'
                    break
    else:
        print(f'[AVISO] hudlayout.res não encontrado em: {caminho_hudlayout}')

    # Salva o resultado no config
    os.makedirs(os.path.join('myhud', 'client_config'), exist_ok=True)
    with open(os.path.join('myhud', 'client_config', 'tem_base_no_hudlayout.txt'), 'w', encoding='utf-8') as f:
        f.write(resultado)

    print(f'[INFO] Resultado salvo: {resultado}')

if __name__ == '__main__':
    try:
        dir_jogo = obter_diretorio_jogo()
        detectar_base_em_hudlayout(dir_jogo)
    except Exception as e:
        print(f"[ERRO] {e}")
