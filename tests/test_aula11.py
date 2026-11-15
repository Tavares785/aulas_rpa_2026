"""Testes de extração e exportação de faturas da AULA11."""

from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from AULA11 import leitor_faturas_pdf


def test_arquivo_do_lab_existe():
    assert leitor_faturas_pdf.__file__
    assert Path(leitor_faturas_pdf.__file__).is_file()


@pytest.mark.parametrize(
    ("texto", "identificador", "valor"),
    [
        (
            "NIF: 501964843\nTotal: 1200.50",
            "501964843",
            "1200.50",
        ),
        (
            "CNPJ: 12.345.678/0001-95\n"
            "Total a pagar: R$ 1.500,00",
            "12.345.678/0001-95",
            "R$ 1.500,00",
        ),
        (
            "CNPJ: 98.765.432/0001-98\n"
            "VALOR TOTAL: R$ 3.640,90",
            "98.765.432/0001-98",
            "R$ 3.640,90",
        ),
    ],
)
def test_extrair_dados(texto, identificador, valor):
    assert leitor_faturas_pdf.extrair_dados(texto, "fatura.pdf") == {
        "arquivo": "fatura.pdf",
        "nif_cnpj": identificador,
        "valor_total": valor,
    }


def test_extrair_dados_preserva_campos_ausentes():
    assert leitor_faturas_pdf.extrair_dados("Sem dados", "vazia.pdf") == {
        "arquivo": "vazia.pdf",
        "nif_cnpj": None,
        "valor_total": None,
    }


def test_ler_texto_concatena_todas_as_paginas(monkeypatch, tmp_path):
    pdf = SimpleNamespace(
        pages=[
            SimpleNamespace(extract_text=lambda: "Página um"),
            SimpleNamespace(extract_text=lambda: "Página dois"),
            SimpleNamespace(extract_text=lambda: None),
        ]
    )
    monkeypatch.setattr(
        leitor_faturas_pdf.pdfplumber,
        "open",
        lambda caminho: nullcontext(pdf),
    )

    assert leitor_faturas_pdf.ler_texto(tmp_path / "fatura.pdf") == (
        "Página um\nPágina dois\n"
    )


def test_extrai_dados_do_pdf_de_exemplo():
    caminho = Path(leitor_faturas_pdf.PASTA_FATURAS) / "fatura_001.pdf"

    assert leitor_faturas_pdf.extrair_dados(
        leitor_faturas_pdf.ler_texto(caminho),
        caminho.name,
    ) == {
        "arquivo": "fatura_001.pdf",
        "nif_cnpj": "12.345.678/0001-95",
        "valor_total": "R$ 1.500,00",
    }


def test_processar_faturas_retorna_um_registro_por_pdf(monkeypatch, tmp_path):
    (tmp_path / "fatura_002.pdf").touch()
    (tmp_path / "fatura_001.pdf").touch()
    (tmp_path / "ignorar.txt").touch()
    textos = {
        "fatura_001.pdf": "NIF: 501964843\nTotal: 1200.50",
        "fatura_002.pdf": "CNPJ: 12.345.678/0001-95\nTotal: R$ 825,75",
    }
    monkeypatch.setattr(
        leitor_faturas_pdf,
        "ler_texto",
        lambda caminho: textos[caminho.name],
    )

    assert leitor_faturas_pdf.processar_faturas(tmp_path) == [
        {
            "arquivo": "fatura_001.pdf",
            "nif_cnpj": "501964843",
            "valor_total": "1200.50",
        },
        {
            "arquivo": "fatura_002.pdf",
            "nif_cnpj": "12.345.678/0001-95",
            "valor_total": "R$ 825,75",
        },
    ]


def test_exportar_excel_salva_colunas_e_registros(tmp_path):
    caminho = tmp_path / "relatorio_faturas.xlsx"
    faturas = [
        {
            "arquivo": "fatura.pdf",
            "nif_cnpj": "501964843",
            "valor_total": "1200.50",
        }
    ]

    leitor_faturas_pdf.exportar_excel(faturas, caminho)

    tabela = pd.read_excel(caminho, dtype=str)
    assert tabela.to_dict(orient="records") == faturas
