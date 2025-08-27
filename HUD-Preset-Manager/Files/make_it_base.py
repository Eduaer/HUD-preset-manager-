import os

# caminhos fixos dos arquivos de controle
TEM_BASE_FILE = os.path.join("myhud", "client_config", "tem_base_no_hudlayout.txt")
MYHUD_FILE = os.path.join("myhud", "client_config", "myhud.txt")

def main():
    # Verifica se o arquivo de controle existe
    if not os.path.exists(TEM_BASE_FILE) or not os.path.exists(MYHUD_FILE):
        print("Arquivos de configuração não encontrados.")
        return
    
    # Lê o conteúdo do tem_base_no_hudlayout.txt
    with open(TEM_BASE_FILE, "r", encoding="utf-8") as f:
        conteudo = f.read().strip().lower()
    
    # Se for "nao", procede
    if conteudo == "nao":
        # Lê o caminho salvo em myhud.txt
        with open(MYHUD_FILE, "r", encoding="utf-8") as f:
            hud_path = f.read().strip()
        
        # Caminho para o arquivo hudlayout.res
        hudlayout_path = os.path.join(hud_path, "scripts", "hudlayout.res")
        
        if not os.path.exists(hudlayout_path):
            print(f"Arquivo não encontrado: {hudlayout_path}")
            return
        
        # Escreve o novo conteúdo no arquivo (apagando o antigo)
        with open(hudlayout_path, "w", encoding="utf-8") as f:
            f.write('#base\t\t"hudlayoutfolder/myhudlayout.res"\n')
        
        print(f"Arquivo {hudlayout_path} modificado com sucesso.")
    else:
        print("O arquivo tem_base_no_hudlayout.txt não contém 'nao'. Nada foi feito.")

if __name__ == "__main__":
    main()
