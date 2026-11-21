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


class TestGmailAPI:
    def test_funcao_smtp(self, source_code):
        assert "enviar_email_smtp" in source_code, (
            "Função enviar_email_smtp não encontrada."
        )

    def test_funcao_gmail_api(self, source_code):
        assert "enviar_email_gmail_api" in source_code, (
            "Função enviar_email_gmail_api não encontrada."
        )

    def test_usa_biblioteca_google(self, source_code):
        assert "googleapiclient" in source_code, (
            "googleapiclient (Google API) não importado."
        )

    def test_escopo_gmail_send(self, source_code):
        assert "gmail.send" in source_code, "Escopo gmail.send não encontrado."

    def test_envia_mensagem_raw(self, source_code):
        assert "messages().send" in source_code.replace(" ", ""), (
            "Chamada users().messages().send não encontrada."
        )
        assert "urlsafe_b64encode" in source_code, (
            "Codificação base64 URL-safe da mensagem não encontrada."
        )

    def test_nao_commita_credenciais(self):
        raiz = SCRIPT_PATH.parent
        for nome in ("credentials.json", "token.json"):
            assert not (raiz / nome).exists(), (
                f"{nome} não deve ser commitado em AULA12/."
            )
