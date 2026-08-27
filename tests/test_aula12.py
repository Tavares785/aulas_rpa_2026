"""
Testes estruturais para AULA12/bot_cotacao_alerta.py.

Valida que:
- O script existe
- Importa requests e email.mime / smtplib
- Consome a API da AwesomeAPI
- Extrai o campo 'bid'
"""

import pathlib

import pytest


SCRIPT_PATH = pathlib.Path(__file__).parent.parent / "AULA12" / "bot_cotacao_alerta.py"


class TestScriptExiste:
    def test_arquivo_existe(self):
        assert SCRIPT_PATH.exists(), "AULA12/bot_cotacao_alerta.py não encontrado."

    def test_arquivo_nao_vazio(self):
        assert SCRIPT_PATH.stat().st_size > 0, "bot_cotacao_alerta.py está vazio."


@pytest.fixture(scope="module")
def source_code():
    if not SCRIPT_PATH.exists():
        pytest.skip("Script não encontrado")
    return SCRIPT_PATH.read_text(encoding="utf-8")


class TestImports:
    def test_importa_requests(self, source_code):
        assert "requests" in source_code, "requests não importado."

    def test_importa_smtplib_ou_mime(self, source_code):
        """O script deve importar smtplib ou email.mime."""
        usa_email = "smtplib" in source_code or "email.mime" in source_code
        assert usa_email, "smtplib ou email.mime não importados."


class TestAPI:
    def test_url_awesomeapi(self, source_code):
        """O script deve consultar a AwesomeAPI."""
        assert "economia.awesomeapi.com.br" in source_code, (
            "URL da AwesomeAPI não encontrada."
        )

    def test_extrai_bid(self, source_code):
        """O script deve extrair o campo 'bid' do JSON."""
        assert "bid" in source_code, "Campo 'bid' não referenciado no script."


class TestEmail:
    def test_funcao_ou_logica_email(self, source_code):
        """O script deve ter lógica de envio/montagem de e-mail."""
        tem_email = "MIME" in source_code or "smtp" in source_code.lower()
        assert tem_email, "Lógica de e-mail (MIME/SMTP) não encontrada."
