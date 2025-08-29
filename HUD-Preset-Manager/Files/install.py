import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys

# Caminho para o python.exe específico
python_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-capado", "python.exe")

subprocess.run([python_exe, 'salvar_hud.py'], check=True)


CAMINHO_BASE = os.path.join('myhud', 'client_config')
CAMINHO_MYHUD = os.path.join(CAMINHO_BASE, 'myhud.txt')
CAMINHO_ESTADO_BASE = os.path.join(CAMINHO_BASE, 'tem_base_no_hudlayout.txt')


def ler_diretorio_cliente():
    """Lê o caminho da HUD salvo em myhud.txt"""
    with open(CAMINHO_MYHUD, 'r', encoding='utf-8') as f:
        return f.read().strip()


def esta_instalado(diretorio_jogo):
    """
    Verifica se existe o arquivo Is_cinhuh_installed.txt dentro da HUD.
    Se não existir, retorna False.
    Se existir e for '1', retorna True.
    """
    caminho_flag = os.path.join(diretorio_jogo, 'Is_cinhuh_installed.txt')
    if not os.path.exists(caminho_flag):
        return False
    with open(caminho_flag, 'r', encoding='utf-8') as f:
        return f.read().strip() == '1'


def ler_estado_base():
    """Verifica o estado do arquivo tem_base_no_hudlayout.txt"""
    if not os.path.exists(CAMINHO_ESTADO_BASE):
        raise Exception('[ERRO] Arquivo tem_base_no_hudlayout.txt não encontrado.')
    with open(CAMINHO_ESTADO_BASE, 'r', encoding='utf-8') as f:
        return f.read().strip().lower() == 'sim'


def executar(script_nome):
    """Executa outro script Python usando o python-capado"""
    caminho_script = os.path.join(script_nome)
    print(f'[INFO] Executando: {caminho_script}')
    subprocess.run([python_exe, caminho_script], check=True)


def mostrar_erro_ui(mensagem):
    """Mostra uma janela de erro com Tkinter e interrompe a execução"""
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showerror("Error", mensagem)
        root.destroy()
    except Exception as e:
        print(f'[ERRO] {mensagem}')
        print(f'[ERRO] Falha ao mostrar interface gráfica: {e}')
    sys.exit(1)  # Força parada do install


def main():
    diretorio_jogo = ler_diretorio_cliente()

    # --- Verifica se já está instalado ---
    if esta_instalado(diretorio_jogo):
        mostrar_erro_ui("You need to revert to your HUD before reinstalling.")
        return  # não chega aqui, porque sys.exit() já encerra

    # --- Executa salvar_hud primeiro ---

    executar('prevent.py')

    # Verificar se o arquivo myhud.txt contém "wrong path"
    try:
        with open(CAMINHO_MYHUD, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()
            if "wrong path" in conteudo.lower():
                mostrar_erro_ui(
                    "Wrong path. If you are using it directly in the tf folder, "
                    "then change it to tf/custom/myhud."
                )
    except Exception as e:
        print(f'[ERRO] Erro ao verificar arquivo myhud.txt: {e}')
        sys.exit(1)

    # --- Continuação da instalação ---
    executar('detectBASEorNOT.py')
    executar('move_hudlayout_and_rename_it.py')
    executar('make_it_base.py')
    executar('copiar_hud.py')
    executar('DoesyourHudDOntHaveHudAnimationsManifestWTF.py')
    executar('injetar_materiais.py')
    executar('detectBASEorNOT.py')
    executar('create_shortcut_auto_start.py')

    if not ler_estado_base():
        executar('encontrar_pos_cl.py')

    print('[OK] Instalação da cinhud concluída com sucesso.')


if __name__ == '__main__':
    main()
