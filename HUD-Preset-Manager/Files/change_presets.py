import os
import shutil
import sys
import subprocess
import stat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PRESETS_DIR = os.path.join(BASE_DIR, "presets", "default_preset")
BACKUP_DIR = os.path.join(BASE_DIR, "backup cinhud", "default_preset")
CUSTOM_PRESETS_DIR = os.path.join(BASE_DIR, "custom presets")

python_exe = os.path.join(BASE_DIR, "python-capado", "python.exe")

# Verificar se o script deve ser executado
install_first_time_path = os.path.join(BASE_DIR, "install_fisrt_time.txt")
cinhud_state_path = os.path.join(BASE_DIR, "cinhud_state.txt")

# Verificar se o arquivo tem_base_no_hudlayout.txt existe e tem conteúdo
hudlayout_check_path = os.path.join(BASE_DIR, "myhud", "client_config", "tem_base_no_hudlayout.txt")
if os.path.exists(hudlayout_check_path):
    try:
        with open(hudlayout_check_path, 'r') as f:
            content = f.read().strip().lower()  # Converter para minúsculas para comparação
        if content == "nao":  # Se o arquivo contém "nao", executar o script
            print("Executando encontrar_pos_cl.py: tem_base_no_hudlayout.txt contém 'nao'")
            subprocess.run([python_exe, os.path.join(BASE_DIR, 'encontrar_pos_cl.py')], shell=True)
        elif content == "sim":  # Se o arquivo contém "sim", não executar o script
            print("Script não executado: tem_base_no_hudlayout.txt contém 'sim'")
        else:
            print(f"Script não executado: tem_base_no_hudlayout.txt contém valor inválido: '{content}'")
    except Exception as e:
        print(f"Erro ao ler tem_base_no_hudlayout.txt: {e}")
else:
    print("Script não executado: arquivo tem_base_no_hudlayout.txt não encontrado")

# Verificar se o arquivo install_first_time.txt existe e ler seu valor
if os.path.exists(install_first_time_path):
    try:
        with open(install_first_time_path, 'r') as f:
            install_value = f.read().strip()
        
        # Se o valor for 0, não executar o script
        if install_value == "0":
            print("Script não executado: install_first_time.txt = 0")
            sys.exit(0)
        elif install_value == "1":
            print("Executando script normalmente: install_first_time.txt = 1")
            # Alterar cinhud_state.txt para 0
            try:
                with open(cinhud_state_path, 'w') as f:
                    f.write("0")
                print("cinhud_state.txt alterado para 0")
            except Exception as e:
                print(f"Erro ao alterar cinhud_state.txt: {e}")
        else:
            print(f"Valor inválido em install_first_time.txt: {install_value}")
            sys.exit(1)
    except Exception as e:
        print(f"Erro ao ler install_first_time.txt: {e}")
        sys.exit(1)
else:
    print("Arquivo install_first_time.txt não encontrado")
    sys.exit(1)

subprocess.run([python_exe, os.path.join(BASE_DIR, "revert.py")], shell=True)




def remover_atributos_readonly(pasta):
    """Remove atributos de somente leitura de todos os arquivos e pastas."""
    if os.path.exists(pasta):
        try:
            # Executa o mesmo comando do CMD: attrib -r /s /d "pasta"
            subprocess.run(['attrib', '-r', '/s', '/d', pasta], shell=True)
        except Exception as e:
            print(f"Erro ao remover atributos: {e}")

def handle_remove_readonly(func, path, exc_info):
    """Callback para forçar exclusão de arquivos somente leitura."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def limpar_pasta(caminho):
    """Remove toda a pasta e recria ela vazia."""
    if os.path.exists(caminho):
        shutil.rmtree(caminho, onerror=handle_remove_readonly)
    os.makedirs(caminho)

def copiar_conteudo(origem, destino):
    """Copia o conteúdo da pasta origem para dentro da pasta destino."""
    for item in os.listdir(origem):
        src = os.path.join(origem, item)
        dst = os.path.join(destino, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

def main(numero):
    if not (0 <= numero <= 20):
        print("Número fora do intervalo permitido (0 a 20).")
        return

    # 1 - Remover atributos somente leitura da pasta alvo
    remover_atributos_readonly(PRESETS_DIR)

    # 2 - Limpar pasta de destino
    limpar_pasta(PRESETS_DIR)

    # 3 - Definir origem
    if numero == 0:
        origem = BACKUP_DIR
    else:
        origem = os.path.join(CUSTOM_PRESETS_DIR, str(numero), "default_preset")

    if not os.path.exists(origem):
        print(f"A pasta de origem não existe: {origem}")
        return

    # 4 - Copiar conteúdo
    copiar_conteudo(origem, PRESETS_DIR)

    print(f"Preset {numero} aplicado com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python esse_script.py <número_de_0_a_20>")
    else:
        try:
            numero = int(sys.argv[1])
            main(numero)
        except ValueError:
            print("Erro: o argumento deve ser um número inteiro.")
