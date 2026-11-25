"""Consulta a cotacao do dolar e a envia por SMTP e pela Gmail API."""

from __future__ import annotations

import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
PASTA = Path(__file__).resolve().parent
CREDENCIAIS = PASTA / "credentials.json"
TOKEN = PASTA / "token.json"


def consultar_cotacao() -> str:
    """Consulta a AwesomeAPI e retorna o valor de compra do dolar."""
    resposta = requests.get(URL_COTACAO, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["USDBRL"]["bid"]


def montar_email(
    cotacao: str, destinatario: str, remetente: str | None = None
) -> MIMEMultipart:
    mensagem = MIMEMultipart()
    mensagem["Subject"] = f"Cotacao atual do dolar: R$ {cotacao}"
    if remetente:
        mensagem["From"] = remetente
    mensagem["To"] = destinatario
    corpo = f"A cotacao de compra do dolar esta em R$ {cotacao}."
    mensagem.attach(MIMEText(corpo, "plain", "utf-8"))
    return mensagem


def exibir_email_mock(mensagem: MIMEMultipart, metodo: str) -> str:
    print(f"[MOCK] E-mail via {metodo}; nenhuma mensagem foi enviada.")
    print(mensagem.as_string())
    return "mock"


def enviar_email_smtp(cotacao: str) -> str:
    """Envia a cotacao por SMTP ou imprime uma simulacao sem credenciais."""
    remetente = os.getenv("EMAIL_REMETENTE", "").strip()
    senha = os.getenv("EMAIL_SENHA_APP", "").strip()
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()
    mensagem = montar_email(
        cotacao,
        destinatario or "(destinatario)",
        remetente or "(remetente)",
    )

    if os.getenv("MOCK_EMAIL", "").lower() == "true" or not all(
        (remetente, senha, destinatario)
    ):
        return exibir_email_mock(mensagem, "SMTP")

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)
    return "enviado"


def enviar_email_gmail_api(cotacao: str) -> str:
    """Envia a cotacao pela Gmail API ou simula se OAuth nao estiver configurado."""
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()
    destinatario_email = destinatario or "(destinatario)"
    mensagem = montar_email(cotacao, destinatario_email)

    if os.getenv("MOCK_EMAIL", "").lower() == "true" or (
        not TOKEN.exists() and not CREDENCIAIS.exists()
    ):
        return exibir_email_mock(mensagem, "Gmail API")

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    credenciais = None
    if TOKEN.exists():
        credenciais = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            if not CREDENCIAIS.exists():
                raise FileNotFoundError(f"Arquivo OAuth nao encontrado: {CREDENCIAIS}")
            fluxo = InstalledAppFlow.from_client_secrets_file(str(CREDENCIAIS), SCOPES)
            credenciais = fluxo.run_local_server(port=0)
        TOKEN.write_text(credenciais.to_json(), encoding="utf-8")
        TOKEN.chmod(0o600)

    servico = build("gmail", "v1", credentials=credenciais)
    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode("ascii")
    servico.users().messages().send(userId="me", body={"raw": raw}).execute()
    return "enviado"


def main() -> int:
    try:
        cotacao = consultar_cotacao()
        print(f"Cotacao atual do dolar (compra): R$ {cotacao}")
    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Falha ao consultar a cotacao: {erro}")
        return 1

    for metodo, enviar in (
        ("SMTP", enviar_email_smtp),
        ("Gmail API", enviar_email_gmail_api),
    ):
        try:
            resultado = enviar(cotacao)
            print(f"Resultado do envio por {metodo}: {resultado}")
        except Exception as erro:
            print(f"Falha no envio por {metodo}: {erro}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
