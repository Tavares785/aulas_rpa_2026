from AULA11 import leitor_faturas_pdf


def test_extrai_nif_cnpj_e_valor_total():
    nif = leitor_faturas_pdf.extrair_dados(
        "Fornecedor NIF 123456789\nTotal: 1500.00", "nif.pdf"
    )
    cnpj = leitor_faturas_pdf.extrair_dados(
        "CNPJ 12.345.678/0001-90\nTotal da fatura: R$ 1.500,00", "cnpj.pdf"
    )

    assert nif == {
        "arquivo": "nif.pdf",
        "nif_cnpj": "123456789",
        "valor_total": "1500.00",
    }
    assert cnpj == {
        "arquivo": "cnpj.pdf",
        "nif_cnpj": "12.345.678/0001-90",
        "valor_total": "R$ 1.500,00",
    }


def test_valor_rotulado_e_priorizado_sobre_outros_valores():
    dados = leitor_faturas_pdf.extrair_dados(
        "Produtos: 25.00\nTotal: 1500.00", "fatura.pdf"
    )

    assert dados["valor_total"] == "1500.00"


def test_processa_faturas_pdf_de_exemplo():
    faturas = leitor_faturas_pdf.processar_faturas()
    por_arquivo = {fatura["arquivo"]: fatura for fatura in faturas}

    assert len(faturas) == 5
    assert por_arquivo["fatura_001.pdf"]["valor_total"] == "R$ 1.500,00"
    assert por_arquivo["fatura_005.pdf"]["nif_cnpj"] is None
    assert por_arquivo["fatura_005.pdf"]["valor_total"] is None


def test_exporta_excel_com_colunas_e_registro(tmp_path):
    caminho = tmp_path / "relatorio_faturas.xlsx"
    faturas = [
        {
            "arquivo": "fatura.pdf",
            "nif_cnpj": "123456789",
            "valor_total": "1500.00",
        }
    ]

    leitor_faturas_pdf.salvar_excel(faturas, caminho)

    planilha = leitor_faturas_pdf.pd.read_excel(caminho, dtype=str)
    assert list(planilha.columns) == ["arquivo", "nif_cnpj", "valor_total"]
    assert planilha.iloc[0].to_dict() == {
        "arquivo": "fatura.pdf",
        "nif_cnpj": "123456789",
        "valor_total": "1500.00",
    }
