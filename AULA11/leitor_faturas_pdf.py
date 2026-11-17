"""
Lab 11 - Extracao de dados de faturas em PDF com regex e exportacao para Excel.

O robo abre cada PDF da pasta faturas/, extrai o texto de todas as paginas
com pdfplumber e usa expressoes regulares para achar:
- o documento do fornecedor: CNPJ (XX.XXX.XXX/XXXX-XX) ou NIF (9 digitos);
- o valor total (formato brasileiro "R$ 1.500,00" ou "Total: 1500.00");
- de quebra, o nome do fornecedor e a data de emissao.

Cada fatura vira um dicionario numa lista, que vira um DataFrame do pandas e
e salvo em relatorio_faturas.xlsx. Fatura sem documento ou sem total nao e
descartada: entra na planilha marcada para revisao manual.

Instalar: pip install pdfplumber pandas openpyxl
Rodar:    python AULA11/leitor_faturas_pdf.py
"""
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PASTA = Path(__file__).resolve().parent
PASTA_FATURAS = PASTA / "faturas"
ARQUIVO_EXCEL = PASTA / "relatorio_faturas.xlsx"

# CNPJ com pontuacao completa: 12.345.678/0001-95
RE_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
# NIF portugues: exatamente 9 digitos seguidos, sem outro digito colado
RE_NIF = re.compile(r"(?<![\d./-])\d{9}(?![\d./-])")
# Linha que contem "total" (Total, Total a pagar, VALOR TOTAL...) e o numero
# logo depois, com ou sem "R$" na frente
RE_TOTAL = re.compile(r"total[^\d\n]*?(R\$\s*)?(\d[\d.,]*\d)", re.IGNORECASE)
RE_FORNECEDOR = re.compile(r"(?:Fornecedor|Raz[aã]o Social):\s*(.+)", re.IGNORECASE)
RE_DATA = re.compile(r"(?:Emiss[aã]o|Data):\s*(\d{2}/\d{2}/\d{4})", re.IGNORECASE)


def extrair_texto(caminho_pdf):
    """Junta o texto de todas as paginas do PDF."""
    with pdfplumber.open(caminho_pdf) as pdf:
        paginas = [pagina.extract_text() or "" for pagina in pdf.pages]
    return "\n".join(paginas)


def buscar_documento(texto):
    """Procura primeiro o CNPJ; se nao houver, tenta o NIF de 9 digitos."""
    cnpj = RE_CNPJ.search(texto)
    if cnpj:
        return "CNPJ", cnpj.group()
    nif = RE_NIF.search(texto)
    if nif:
        return "NIF", nif.group()
    return None, None


def para_numero(valor_texto, tem_simbolo_real):
    """Converte '1.500,00' (BR) ou '1200.50' (internacional) em float."""
    if tem_simbolo_real or "," in valor_texto:
        valor_texto = valor_texto.replace(".", "").replace(",", ".")
    return float(valor_texto)


def buscar_total(texto):
    """Acha o valor total e devolve como float (ou None)."""
    achado = RE_TOTAL.search(texto)
    if not achado:
        return None
    return para_numero(achado.group(2), achado.group(1) is not None)


def buscar_primeiro(regex, texto):
    achado = regex.search(texto)
    return achado.group(1).strip() if achado else None


def ler_fatura(caminho_pdf):
    """Extrai os campos de uma fatura e devolve um dicionario."""
    texto = extrair_texto(caminho_pdf)
    tipo_documento, documento = buscar_documento(texto)
    total = buscar_total(texto)

    pendencias = []
    if documento is None:
        pendencias.append("documento nao encontrado")
    if total is None:
        pendencias.append("total nao encontrado")

    return {
        "arquivo": caminho_pdf.name,
        "fornecedor": buscar_primeiro(RE_FORNECEDOR, texto),
        "data_emissao": buscar_primeiro(RE_DATA, texto),
        "tipo_documento": tipo_documento,
        "documento": documento,
        "valor_total": total,
        "status": "REVISAO MANUAL: " + ", ".join(pendencias) if pendencias else "OK",
    }


def main():
    arquivos = sorted(PASTA_FATURAS.glob("*.pdf"))
    if not arquivos:
        print(f"Nenhum PDF encontrado em {PASTA_FATURAS}")
        return

    faturas = []
    for caminho in arquivos:
        fatura = ler_fatura(caminho)
        faturas.append(fatura)
        print(f"{fatura['arquivo']}: {fatura['tipo_documento'] or '-'} "
              f"{fatura['documento'] or '-'} | total {fatura['valor_total']} "
              f"| {fatura['status']}")

    tabela = pd.DataFrame(faturas)
    tabela.to_excel(ARQUIVO_EXCEL, index=False, sheet_name="faturas")

    ok = tabela[tabela["status"] == "OK"]
    print(f"\n{len(tabela)} faturas lidas, {len(ok)} ok, "
          f"{len(tabela) - len(ok)} para revisao manual.")
    soma = f"{ok['valor_total'].sum():,.2f}"
    soma_br = soma.replace(",", "_").replace(".", ",").replace("_", ".")
    print(f"Soma das faturas ok: R$ {soma_br}")
    print(f"Relatorio salvo em {ARQUIVO_EXCEL.name}")


if __name__ == "__main__":
    main()
