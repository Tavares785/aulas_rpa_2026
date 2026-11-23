"""
Lab 12 - cotacao do dolar e notificacao por e-mail.
"""

from __future__ import annotations

import base64
import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path

import requests


URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
PASTA_AULA = Path(__file__).resolve().parent
ARQUIVO_CREDENCIAIS = Path(
    os.getenv("GOOGLE_CREDENTIALS_FILE", PASTA_AULA / "credentials.json")
)
ARQUIVO_TOKEN = Path(os.getenv("GOOGLE_TOKEN_FILE", PASTA_AULA / "token.json"))


def obter_cotacao() -> str:
    """Consulta a AwesomeAPI e retorna o valor de compra (bid)."""
    resposta = requests.get(URL_COTACAO, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["USDBRL"]["bid"]


def montar_mensagem(cotacao: str) -> MIMEText:
    """Monta a mensagem usada pelos dois metodos de envio."""
    remetente = os.getenv("EMAIL_REMETENTE", "")
    destinatario = os.getenv("EMAIL_DESTINATARIO", "")

    mensagem = MIMEText(
        f"Cotacao atual do dolar: R$ {cotacao}",
        _subtype="plain",
        _charset="utf-8",
    )
    mensagem["Subject"] = "Alerta de cotacao do Dolar"
    mensagem["From"] = remetente or "remetente-nao-configurado"
    mensagem["To"] = destinatario or "destinatario-nao-configurado"
    return mensagem


def exibir_mock_email(cotacao: str, metodo: str) -> None:
    """Imprime o e-mail sem enviarlo quando o modo mock estiver ativo."""
    mensagem = montar_mensagem(cotacao)
    print(f"[MOCK] E-mail para {mensagem['To']} via {metodo}")
    print(f"[MOCK] Assunto: {mensagem['Subject']}")
    print(f"[MOCK] Corpo: Cotacao atual do dolar: R$ {cotacao}")


def enviar_email_smtp(cotacao: str) -> str:
    """Envia o alerta pelo SMTP do Gmail."""
    if os.getenv("MOCK_EMAIL", "").lower() == "true":
        exibir_mock_email(cotacao, "SMTP")
        return "E-mail SMTP exibido em modo mock."

    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    if not all((remetente, senha_app, destinatario)):
        exibir_mock_email(cotacao, "SMTP")
        return "Credenciais SMTP ausentes; e-mail exibido em modo mock."

    mensagem = montar_mensagem(cotacao)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha_app)
        servidor.send_message(mensagem)
    return "E-mail enviado via SMTP."


def enviar_email_gmail_api(cotacao: str) -> str:
    """Envia o alerta pela Gmail API usando OAuth 2.0."""
    if os.getenv("MOCK_EMAIL", "").lower() == "true":
        exibir_mock_email(cotacao, "Gmail API")
        return "E-mail Gmail API exibido em modo mock."

    destinatario = os.getenv("EMAIL_DESTINATARIO")
    if not destinatario:
        exibir_mock_email(cotacao, "Gmail API")
        return "EMAIL_DESTINATARIO ausente; e-mail exibido em modo mock."

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    credenciais = None
    if ARQUIVO_TOKEN.exists():
        credenciais = Credentials.from_authorized_user_file(
            str(ARQUIVO_TOKEN), SCOPES
        )

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            if not ARQUIVO_CREDENCIAIS.exists():
                exibir_mock_email(cotacao, "Gmail API")
                return (
                    "credentials.json ausente; e-mail exibido em modo mock."
                )
            fluxo = InstalledAppFlow.from_client_secrets_file(
                str(ARQUIVO_CREDENCIAIS), SCOPES
            )
            credenciais = fluxo.run_local_server(port=0)

        ARQUIVO_TOKEN.write_text(credenciais.to_json(), encoding="utf-8")

    servico = build("gmail", "v1", credentials=credenciais)
    mensagem = montar_mensagem(cotacao)
    bruto = base64.urlsafe_b64encode(mensagem.as_bytes()).decode("ascii")
    resposta = servico.users().messages().send(
        userId="me", body={"raw": bruto}
    ).execute()
    return f"E-mail enviado pela Gmail API (id: {resposta['id']})."


def main() -> int:
    try:
        cotacao = obter_cotacao()
        print(f"Cotacao atual do dolar: R$ {cotacao}")
    except requests.RequestException as erro:
        print(f"Falha ao consultar a API: {erro}")
        return 1
    except (KeyError, ValueError) as erro:
        print(f"Falha ao processar a resposta da API: {erro}")
        return 1

    try:
        resultado_smtp = enviar_email_smtp(cotacao)
        print(f"SMTP: {resultado_smtp}")
    except Exception as erro:  # noqa: BLE001 - isolar falhas dos metodos
        print(f"SMTP: falha no envio: {erro}")

    try:
        resultado_gmail = enviar_email_gmail_api(cotacao)
        print(f"Gmail API: {resultado_gmail}")
    except Exception as erro:  # noqa: BLE001 - isolar falhas dos metodos
        print(f"Gmail API: falha no envio: {erro}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
