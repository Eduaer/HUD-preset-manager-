import tkinter as tk
from tkinter import filedialog
import os

def escolher_pasta_origem():
    tk.Tk().withdraw()  # Oculta a janela principal
    pasta = filedialog.askdirectory(title="Selecione a pasta da sua HUD personalizada")
    return pasta

def salvar_diretorio_hud(origem):
    config_dir = os.path.join('myhud', 'client_config')
    os.makedirs(config_dir, exist_ok=True)

    caminho_arquivo = os.path.join(config_dir, 'myhud.txt')

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.write(origem)

    print(f'Caminho da HUD salvo em: {caminho_arquivo}')

if __name__ == '__main__':
    origem = escolher_pasta_origem()
    if origem:
        salvar_diretorio_hud(origem)
    else:
        print("Nenhuma pasta foi selecionada.")
