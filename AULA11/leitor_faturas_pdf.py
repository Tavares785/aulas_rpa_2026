import re
from pathlib import Path
import pandas as pd
import pdfplumber


def extrair_nif_cnpj(texto: str) -> str | None:
    padrao = r"\b(?:\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{9})\b"
    match = re.search(padrao, texto)
    return match.group(0) if match else None


def extrair_valor_total(texto: str) -> str | None:
    padrao = (
        r"(?:valor\s*total|total|r\$)?\s*:?\s*"
        r"((?:\d{1,3}(?:\.\d{3})*|\d+)(?:,\d{2}|\.\d{2}))"
    )
    match = re.search(padrao, texto, flags=re.IGNORECASE)
    if not match:
        return None
    # Retorna o valor formatado com prefixo se houver, ou apenas o número capturado
    return match.group(0).strip()


def normalizar_numero_para_excel(valor_str: str | None) -> float | None:
    if not valor_str:
        return None

    #  Só isola dígitos, pontos e vírgulas
    limpo = re.sub(r"[^\d.,]", "", valor_str)
    if not limpo:
        return None

    # Caso tenha vírgula e ponto (ex.: 1.500,00) -> remove pontos de milhar e troca vírgula por ponto
    if "," in limpo and "." in limpo:
        if limpo.rfind(",") > limpo.rfind("."):
            limpo = limpo.replace(".", "").replace(",", ".")
        else:
            limpo = limpo.replace(",", "")
    elif "," in limpo:
        # Apenas vírgula (ex.: 1500,00)
        limpo = limpo.replace(",", ".")

    try:
        return float(limpo)
    except ValueError:
        return None


def processar_faturas() -> None:
    # Pasta onde este script está localizado
    pasta_base = Path(__file__).resolve().parent
    pasta_faturas = pasta_base / "faturas"
    arquivo_excel = pasta_base / "relatorio_faturas.xlsx"

    if not pasta_faturas.exists():
        print(f"Aviso: a pasta '{pasta_faturas}' não foi encontrada.")
        return

    arquivos_pdf = sorted(pasta_faturas.glob("*.pdf"))
    if not arquivos_pdf:
        print(f"Nenhum arquivo PDF encontrado em '{pasta_faturas}'.")
        return

    registros: list[dict] = []

    for caminho_pdf in arquivos_pdf:
        texto_completo_paginas: list[str] = []

        with pdfplumber.open(caminho_pdf) as pdf:
            for indice_pagina, pagina in enumerate(pdf.pages, start=1):
                texto_pagina = pagina.extract_text() or ""
                texto_completo_paginas.append(
                    f"--- Página {indice_pagina} ---\n{texto_pagina}"
                )

        texto_fatura = "\n".join(texto_completo_paginas)

        nif_cnpj = extrair_nif_cnpj(texto_fatura)
        valor_bruto = extrair_valor_total(texto_fatura)
        valor_numerico = normalizar_numero_para_excel(valor_bruto)

        fatura_dict = {
            "arquivo_pdf": caminho_pdf.name,
            "nif_cnpj": nif_cnpj,
            "valor_total_extraido": valor_bruto,
            "valor_total_numerico": valor_numerico,
        }
        registros.append(fatura_dict)

    # Converte a lista de dicionários em DataFrame do pandas
    df = pd.DataFrame(registros)

    # Exporta para Excel utilizando o engine openpyxl
    with pd.ExcelWriter(arquivo_excel, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Faturas", index=False)

    print(f"Processamento concluído! Relatório salvo em: {arquivo_excel}")


if __name__ == "__main__":
    processar_faturas()