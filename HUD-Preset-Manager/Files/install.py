import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import sys

# Caminho para o python.exe específico
python_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "python-capado", "python.exe")

CAMINHO_BASE = os.path.join('myhud', 'client_config')
CAMINHO_MYHUD = os.path.join(CAMINHO_BASE, 'myhud.txt')
CAMINHO_ESTADO_BASE = os.path.join(CAMINHO_BASE, 'tem_base_no_hudlayout.txt')

def ler_diretorio_cliente():
    with open(CAMINHO_MYHUD, 'r', encoding='utf-8') as f:
        return f.read().strip()

def esta_instalado(diretorio_jogo):
    caminho_flag = os.path.join(diretorio_jogo, 'Is_cinhuh_installed.txt')
    if not os.path.exists(caminho_flag):
        return False  # Considerar como não instalado
    with open(caminho_flag, 'r', encoding='utf-8') as f:
        return f.read().strip() == '1'

def ler_estado_base():
    if not os.path.exists(CAMINHO_ESTADO_BASE):
        raise Exception('[ERRO] Arquivo tem_base_no_hudlayout.txt não encontrado.')
    with open(CAMINHO_ESTADO_BASE, 'r', encoding='utf-8') as f:
        return f.read().strip().lower() == 'sim'

def executar(script_nome):
    caminho_script = os.path.join(script_nome)
    print(f'[INFO] Executando: {caminho_script}')
    subprocess.run([python_exe, caminho_script], check=True)

def mostrar_erro_ui(mensagem):
    """Função para mostrar erro na UI de forma robusta"""
    try:
        # Tentar usar Tkinter
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        root.focus_force()
        
        # Configurar a janela para aparecer no centro
        root.geometry("1x1+{}+{}".format(
            root.winfo_screenwidth()//2,
            root.winfo_screenheight()//2
        ))
        
        # Mostrar a mensagem de erro
        messagebox.showerror("Erro", mensagem)
        
        # Aguardar um pouco antes de destruir a janela
        root.after(500, root.destroy)
        root.mainloop()
        
    except Exception as e:
        # Fallback: usar apenas print se Tkinter falhar
        print(f'[ERRO] {mensagem}')
        print(f'[ERRO] Falha ao mostrar interface gráfica: {e}')
        
        # Tentar uma abordagem alternativa com subprocess
        try:
            import subprocess
            if os.name == 'nt':  # Windows
                subprocess.run(['cmd', '/c', 'echo', mensagem, '&&', 'pause'], shell=True)
            else:  # Linux/Mac
                subprocess.run(['echo', mensagem], check=True)
        except:
            pass  # Se tudo falhar, pelo menos o print funcionou

def main():
    diretorio_jogo = ler_diretorio_cliente()

    if esta_instalado(diretorio_jogo):
        print('[ERROR] Reversal required before reinstalling.')
        return

    executar('salvar_hud.py')
    executar('prevent.py')
    
    # Verificar se o arquivo myhud.txt contém "wrong path"
    try:
        with open(CAMINHO_MYHUD, 'r', encoding='utf-8') as f:
            conteudo = f.read().strip()
            if "wrong path" in conteudo.lower():
                mostrar_erro_ui("wrong path, If you are using it directly in the tf folder, then change it to tf/custom/myhud.")
                sys.exit(1)
    except Exception as e:
        print(f'[ERRO] Erro ao verificar arquivo myhud.txt: {e}')
        sys.exit(1)
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