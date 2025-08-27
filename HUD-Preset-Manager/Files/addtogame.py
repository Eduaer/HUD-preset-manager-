import os
import subprocess

# Caminho para o python.exe específico
python_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-capado", "python.exe")

CAMINHO_BASE = os.path.join('myhud', 'client_config')
CAMINHO_ESTADO_BASE = os.path.join(CAMINHO_BASE, 'tem_base_no_hudlayout.txt')
CAMINHO_MYHUD = os.path.join(CAMINHO_BASE, 'myhud.txt')

def ler_diretorio_cliente():
    with open(CAMINHO_MYHUD, 'r', encoding='utf-8') as f:
        return f.read().strip()

def marcar_cinhud_como_instalada(diretorio_jogo):
    caminho_flag = os.path.join(diretorio_jogo, 'Is_cinhuh_installed.txt')
    with open(caminho_flag, 'w', encoding='utf-8') as f:
        f.write('1')

def ler_estado_base():
    if not os.path.exists(CAMINHO_ESTADO_BASE):
        raise Exception('[ERRO] Arquivo tem_base_no_hudlayout.txt não encontrado.')
    with open(CAMINHO_ESTADO_BASE, 'r', encoding='utf-8') as f:
        return f.read().strip().lower() == 'sim'

def executar(script_nome):
    caminho_script = os.path.join(script_nome)
    print(f'[INFO] Executando: {caminho_script}')
    subprocess.run([python_exe, caminho_script], check=True)

def main():
    diretorio_jogo = ler_diretorio_cliente()
    tem_base = ler_estado_base()

    if tem_base:
        executar('hudlayoutBASEinject.py')
    else:
        executar('escrever_hudlayout.py')

    executar('cinHud_to_game.py')
    executar('in_animations.py')
    marcar_cinhud_como_instalada(diretorio_jogo)
    print('[OK] Cinhud adicionada ao jogo com sucesso.')

if __name__ == '__main__':
    main()