from pathlib import Path

def main() -> None:
    arquivo = Path(__file__).parent / "install_fisrt_time.txt"
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

    conteudo = arquivo.read_text(encoding="utf-8")
    if conteudo.strip() != "0":
        return

    if "\r\n" in conteudo:
        fim_de_linha = "\r\n"
    elif "\n" in conteudo:
        fim_de_linha = "\n"
    else:
        fim_de_linha = ""

    arquivo.write_text("1" + fim_de_linha, encoding="utf-8")

if __name__ == "__main__":
    main()