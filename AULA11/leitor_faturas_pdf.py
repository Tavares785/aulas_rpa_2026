"""
Lab 11 - Extração de Dados em PDFs, Filtros Regex e Exportação para Excel
Aluno: Icaro Ferrari de Senço - RA 1926102

Pipeline:
1. Lê as faturas em PDF da pasta faturas/ (pdfplumber), página a página.
   Se a pasta estiver vazia, gera faturas de exemplo para simular a caixa de entrada.
2. Usa expressões regulares (re.search) para isolar NIF/CNPJ, data e valor total.
3. Guarda cada fatura em uma lista de dicionários.
4. Converte em DataFrame (pandas) e salva em relatorio_faturas.xlsx.
"""

import logging
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PASTA_BASE = Path(__file__).resolve().parent
PASTA_FATURAS = PASTA_BASE / "faturas"
ARQUIVO_EXCEL = PASTA_BASE / "relatorio_faturas.xlsx"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ---------------------------------------------------------------------------
# Expressões regulares
# ---------------------------------------------------------------------------
# CNPJ no formato XX.XXX.XXX/XXXX-XX
REGEX_CNPJ = re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b")
# NIF: exatamente 9 dígitos (não faz parte de um número maior)
REGEX_NIF = re.compile(r"(?<![\d.,/-])\d{9}(?![\d.,/-])")
# Valor total: "R$ 1.500,00" ou "Total: 1500.00"
REGEX_VALOR_BRL = re.compile(r"R\$\s*(\d{1,3}(?:\.\d{3})*,\d{2}|\d+,\d{2})")
REGEX_VALOR_TOTAL = re.compile(r"Total\s*:?\s*(?:R\$\s*)?(\d+(?:[.,]\d{3})*[.,]\d{2})", re.IGNORECASE)
# Data de emissão: dd/mm/aaaa
REGEX_DATA = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")


# ---------------------------------------------------------------------------
# Faturas de exemplo (simulação da caixa de entrada)
# ---------------------------------------------------------------------------
FATURAS_EXEMPLO = {
    "fatura_001.pdf": [
        "FATURA N. 001",
        "Fornecedor: Concreteira Atibaia Ltda",
        "CNPJ: 12.345.678/0001-90",
        "Data de emissao: 03/11/2026",
        "Descricao: 12 m3 de concreto usinado fck 25 MPa",
        "Valor Total: R$ 6.480,00",
    ],
    "fatura_002.pdf": [
        "INVOICE / FATURA 002",
        "Supplier: Lisboa Materiais SA",
        "NIF: 509876543",
        "Data: 05/11/2026",
        "Item: Aco CA-50 10 mm - 850 kg",
        "Total: 1500.00",
    ],
    "fatura_003.pdf": [
        "FATURA N. 003",
        "Fornecedor: Locadora de Equipamentos Braganca",
        "CNPJ: 98.765.432/0001-10",
        "Emissao: 10/11/2026",
        "Locacao de betoneira 400 L - 15 dias",
        "Subtotal: R$ 1.200,00",
        "Desconto: R$ 100,00",
        "Total: R$ 1.100,00",
    ],
}


def _escapar_pdf(texto):
    return texto.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def criar_pdf_simples(caminho, linhas):
    """Gera um PDF de uma página com texto, sem bibliotecas extras."""
    conteudo = ["BT", "/F1 12 Tf", "72 760 Td", "16 TL"]
    for linha in linhas:
        conteudo.append(f"({_escapar_pdf(linha)}) Tj T*")
    conteudo.append("ET")
    stream = "\n".join(conteudo).encode("latin-1")

    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for numero, obj in enumerate(objetos, start=1):
        offsets.append(len(pdf))
        pdf += f"{numero} 0 obj\n".encode() + obj + b"\nendobj\n"

    inicio_xref = len(pdf)
    pdf += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode()
    for offset in offsets:
        pdf += f"{offset:010d} 00000 n \n".encode()
    pdf += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\n".encode()
    pdf += f"startxref\n{inicio_xref}\n%%EOF\n".encode()

    Path(caminho).write_bytes(bytes(pdf))


def preparar_faturas():
    """Garante que existam PDFs na pasta faturas/ (gera exemplos se estiver vazia)."""
    PASTA_FATURAS.mkdir(exist_ok=True)
    pdfs = sorted(PASTA_FATURAS.glob("*.pdf"))
    if pdfs:
        return pdfs

    logging.info("Pasta faturas/ vazia. Gerando %d faturas de exemplo...", len(FATURAS_EXEMPLO))
    for nome, linhas in FATURAS_EXEMPLO.items():
        criar_pdf_simples(PASTA_FATURAS / nome, linhas)
    return sorted(PASTA_FATURAS.glob("*.pdf"))


# ---------------------------------------------------------------------------
# Extração
# ---------------------------------------------------------------------------
def extrair_texto_pdf(caminho):
    """Extrai o texto de todas as páginas do PDF."""
    paginas = []
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            paginas.append(pagina.extract_text() or "")
    return "\n".join(paginas)


def valor_para_float(valor_texto):
    """Converte '1.500,00' ou '1500.00' em 1500.0."""
    if "," in valor_texto:
        valor_texto = valor_texto.replace(".", "").replace(",", ".")
    else:
        valor_texto = valor_texto.replace(",", "")
    return float(valor_texto)


def encontrar_documento(texto):
    """Retorna (tipo, número) do CNPJ ou NIF encontrado."""
    cnpj = re.search(REGEX_CNPJ, texto)
    if cnpj:
        return "CNPJ", cnpj.group()
    nif = re.search(REGEX_NIF, texto)
    if nif:
        return "NIF", nif.group()
    return "", ""


def encontrar_valor_total(texto):
    """Prioriza a linha de 'Total'; se não houver, usa o maior valor em R$."""
    totais = re.findall(REGEX_VALOR_TOTAL, texto)
    if totais:
        return valor_para_float(totais[-1])

    valores = [valor_para_float(v) for v in re.findall(REGEX_VALOR_BRL, texto)]
    return max(valores) if valores else None


def processar_fatura(caminho):
    texto = extrair_texto_pdf(caminho)
    tipo_doc, documento = encontrar_documento(texto)
    data = re.search(REGEX_DATA, texto)
    valor = encontrar_valor_total(texto)

    status = "OK" if documento and valor is not None else "REVISAR"
    if status == "REVISAR":
        logging.warning("%s: dados incompletos, revisar manualmente.", caminho.name)

    return {
        "arquivo": caminho.name,
        "tipo_documento": tipo_doc,
        "documento": documento,
        "data_emissao": data.group(1) if data else "",
        "valor_total": valor,
        "status": status,
    }


def main():
    faturas = []
    for caminho in preparar_faturas():
        try:
            dados = processar_fatura(caminho)
        except Exception as erro:
            logging.error("Erro ao ler %s: %s", caminho.name, erro)
            continue
        faturas.append(dados)
        logging.info("%s -> %s %s | R$ %s", caminho.name, dados["tipo_documento"],
                     dados["documento"], dados["valor_total"])

    if not faturas:
        logging.error("Nenhuma fatura processada.")
        return

    df = pd.DataFrame(faturas)
    df.to_excel(ARQUIVO_EXCEL, index=False, sheet_name="Faturas", engine="openpyxl")

    print("\n" + df.to_string(index=False))
    print(f"\nTotal geral: R$ {df['valor_total'].sum():,.2f}")
    print(f"Relatório salvo em: {ARQUIVO_EXCEL.name}")


if __name__ == "__main__":
    main()
