"""
Módulo para automação de consulta à cotação do Dólar e envio de alertas por e-mail.

Lab 12:
- Consome a API pública da AwesomeAPI (USD-BRL) e extrai a cotação de compra ('bid').
- Envia notificação por e-mail via protocolo SMTP (smtplib e email.mime).
- Envia notificação por e-mail via Gmail API (Google API) com OAuth 2.0.
"""

from __future__ import annotations

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    Request = None
    Credentials = None
    InstalledAppFlow = None
    build = None

import requests

URL_AWESOMEAPI = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def obter_cotacao_dolar() -> str:
    """Consulta a AwesomeAPI e retorna o valor de compra ('bid') do Dólar."""
    resposta = requests.get(URL_AWESOMEAPI, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["USDBRL"]["bid"]


def montar_mensagem_email(cotacao: str, destinatario: str, remetente: str = "") -> MIMEMultipart:
    """Monta a estrutura da mensagem de e-mail usando email.mime."""
    msg = MIMEMultipart()
    msg["Subject"] = f"Alerta de Cotação: Dólar a R$ {cotacao}"
    if remetente:
        msg["From"] = remetente
    msg["To"] = destinatario

    corpo = (
        f"Olá,\n\n"
        f"Este é um alerta automático de cotação de moeda.\n"
        f"Cotação atual de compra (bid) do Dólar (USD-BRL): R$ {cotacao}\n\n"
        f"Atenciosamente,\n"
        f"Robô de Cotações"
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    return msg


def enviar_email_smtp(cotacao: str) -> None:
    """Envia notificação de e-mail utilizando protocolo SMTP (smtplib e email.mime)."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not remetente or not senha or not destinatario:
        print("[SMTP - MOCK] Variáveis de ambiente não configuradas (EMAIL_REMETENTE, EMAIL_SENHA_APP, EMAIL_DESTINATARIO).")
        print(f"[SMTP - MOCK] Simulação: e-mail com cotação R$ {cotacao} gerado com sucesso.")
        return

    msg = montar_mensagem_email(cotacao, destinatario=destinatario, remetente=remetente)
    servidor_smtp = "smtp.gmail.com"
    porta = 587

    with smtplib.SMTP(servidor_smtp, porta) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)

    print(f"[SMTP] E-mail enviado com sucesso para {destinatario}!")


def enviar_email_gmail_api(cotacao: str) -> None:
    """Envia notificação de e-mail utilizando a Gmail API (Google API) com OAuth 2.0."""
    pasta = Path(__file__).resolve().parent
    credenciais_path = pasta / "credentials.json"
    token_path = pasta / "token.json"

    destinatario = os.getenv("EMAIL_DESTINATARIO", "")

    if build is None:
        print("[Gmail API - MOCK] Bibliotecas google-api-python-client/google-auth não instaladas.")
        print(f"[Gmail API - MOCK] Simulação: e-mail com cotação R$ {cotacao} gerado com sucesso.")
        return

    if not token_path.exists() and not credenciais_path.exists():
        print("[Gmail API - MOCK] Arquivos credentials.json e token.json não encontrados.")
        print(f"[Gmail API - MOCK] Simulação: e-mail com cotação R$ {cotacao} gerado com sucesso.")
        return

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), GMAIL_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credenciais_path.exists():
                raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {credenciais_path}")
            fluxo = InstalledAppFlow.from_client_secrets_file(str(credenciais_path), GMAIL_SCOPES)
            creds = fluxo.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    service = build("gmail", "v1", credentials=creds)

    if not destinatario:
        perfil = service.users().getProfile(userId="me").execute()
        destinatario = perfil.get("emailAddress", "")

    msg = montar_mensagem_email(cotacao, destinatario=destinatario)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")

    resposta = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print(f"[Gmail API] E-mail enviado com sucesso! ID da mensagem: {resposta.get('id')}")


def main() -> None:
    """Execução principal do bot integrador de cotação e alerta."""
    print("Iniciando Bot de Cotação e Alerta...")
    try:
        cotacao = obter_cotacao_dolar()
        print(f"Cotação do Dólar obtida com sucesso: R$ {cotacao}")
    except Exception as erro:
        print(f"Erro ao consultar a AwesomeAPI: {erro}")
        return

    print("\n--- 1. Envio via SMTP ---")
    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:
        print(f"Falha no envio via SMTP: {erro}")

    print("\n--- 2. Envio via Gmail API ---")
    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro:
        print(f"Falha no envio via Gmail API: {erro}")


if __name__ == "__main__":
    main()

