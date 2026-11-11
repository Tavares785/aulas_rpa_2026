"""
AULA 11 - Gerador de PDFs (apoio do PROFESSOR)

Converte cada .txt em um PDF real (sem dependencias externas) em:
  - AULA11/faturas/               (entrada do trabalho de casa dos alunos)
  - lab-professor/AULA11/espelhos/ (entrada do exemplo da aula)
Uso: python gerar_faturas_pdf.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PASTAS = [
    RAIZ / "AULA11" / "faturas",
    Path(__file__).resolve().parent / "espelhos",
]


def _escapar(linha: str) -> str:
    return linha.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def montar_pdf(linhas: list) -> bytes:
    """Monta um PDF de 1 pagina (Courier 11pt) com as linhas informadas."""
    fluxo = ["BT", "/F1 11 Tf", "14 TL", "50 790 Td"]
    for linha in linhas:
        fluxo.append(f"({_escapar(linha)}) Tj T*")
    fluxo.append("ET")
    conteudo = "\n".join(fluxo).encode("cp1252", errors="replace")

    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier "
        b"/Encoding /WinAnsiEncoding >>",
        b"<< /Length " + str(len(conteudo)).encode() + b" >>\nstream\n"
        + conteudo + b"\nendstream",
    ]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objetos, start=1):
        offsets.append(len(pdf))
        pdf += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(pdf)
    pdf += f"xref\n0 {len(objetos) + 1}\n".encode()
    pdf += b"0000000000 65535 f \n"
    for off in offsets:
        pdf += f"{off:010d} 00000 n \n".encode()
    pdf += (
        f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode()
    return bytes(pdf)


if __name__ == "__main__":
    for pasta in PASTAS:
        for txt in sorted(pasta.glob("*.txt")):
            linhas = txt.read_text(encoding="utf-8").splitlines()
            destino = txt.with_suffix(".pdf")
            destino.write_bytes(montar_pdf(linhas))
            print(f"Gerado: {destino.relative_to(RAIZ)}")
