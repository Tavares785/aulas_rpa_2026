"""
AULA 12 - Integracao de Sistemas via APIs REST e Notificacoes por E-mail

Cenario de negocio: o bot consulta a cotacao atual do Dolar (USD-BRL) na
AwesomeAPI e dispara um alerta por e-mail usando dois canais - SMTP
(smtplib) e Gmail API (OAuth2) - para comparar as duas formas de envio.

Requer:
    pip install requests google-api-python-client google-auth-httplib2 \
        google-auth-oauthlib
"""
from __future__ import annotations

import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

API_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA = Path(__file__).resolve().parent
CREDENCIAIS = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", PASTA / "credentials.json"))
TOKEN = Path(os.getenv("GOOGLE_TOKEN_FILE", PASTA / "token.json"))


def consultar_cotacao_dolar() -> str:
    """GET na AwesomeAPI; devolve o valor de compra ('bid') do USD-BRL."""
    resposta = requests.get(API_COTACAO, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["USDBRL"]["bid"]


def _montar_mensagem(cotacao: str, remetente: str, destinatario: str) -> MIMEMultipart:
    """Monta a mensagem de e-mail com email.mime."""
    msg = MIMEMultipart()
    msg["Subject"] = "Alerta de Cotacao: Dolar (USD-BRL)"
    msg["From"] = remetente
    msg["To"] = destinatario
    corpo = (
        "Alerta automatico de cotacao:\n\n"
        f"Dolar (USD/BRL) - valor de compra (bid): R$ {cotacao}\n"
    )
    msg.attach(MIMEText(corpo, _subtype="plain", _charset="utf-8"))
    return msg


def enviar_email_smtp(cotacao: str) -> str:
    """Envia o alerta de cotacao via SMTP (smtp.gmail.com, porta 587, STARTTLS)."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    msg = _montar_mensagem(
        cotacao,
        remetente or "(EMAIL_REMETENTE nao configurado)",
        destinatario or "(EMAIL_DESTINATARIO nao configurado)",
    )

    if not remetente or not senha_app or not destinatario:
        print("[MOCK - SMTP] Credenciais nao configuradas. E-mail que seria enviado:")
        print(msg.as_string())
        return "mock"

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha_app)
        servidor.sendmail(remetente, destinatario, msg.as_string())
    return "enviado"


def _obter_servico_gmail():
    """Autentica via OAuth2 (reusa/renova token.json) e devolve o cliente Gmail."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(str(CREDENCIAIS), SCOPES)
            creds = fluxo.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def enviar_email_gmail_api(cotacao: str) -> str:
    """Envia o alerta de cotacao pela Gmail API (users().messages().send)."""
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    msg = _montar_mensagem(
        cotacao,
        "(preenchido automaticamente pela conta Gmail)",
        destinatario or "(EMAIL_DESTINATARIO nao configurado)",
    )

    if not CREDENCIAIS.exists():
        print("[MOCK - Gmail API] credentials.json nao encontrado. E-mail que seria enviado:")
        print(msg.as_string())
        return "mock"

    servico = _obter_servico_gmail()
    bruto = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    resposta = servico.users().messages().send(userId="me", body={"raw": bruto}).execute()
    return resposta["id"]


def main() -> None:
    try:
        cotacao = consultar_cotacao_dolar()
        print(f"Cotacao atual do Dolar (bid): R$ {cotacao}")
    except requests.RequestException as erro:
        print(f"Nao foi possivel consultar a cotacao na AwesomeAPI: {erro}")
        return

    try:
        resultado_smtp = enviar_email_smtp(cotacao)
        print(f"[SMTP] Resultado do envio: {resultado_smtp}")
    except Exception as erro:  # noqa: BLE001 - falha de rede/autenticacao SMTP
        print(f"[SMTP] Falha ao enviar e-mail: {erro}")

    try:
        resultado_gmail = enviar_email_gmail_api(cotacao)
        print(f"[Gmail API] Resultado do envio: {resultado_gmail}")
    except Exception as erro:  # noqa: BLE001 - HttpError, erros de OAuth, rede
        print(f"[Gmail API] Falha ao enviar e-mail: {erro}")


if __name__ == "__main__":
    main()
