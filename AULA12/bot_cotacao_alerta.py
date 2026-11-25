"""
Lab 12: Integração de Sistemas via APIs REST e Notificações por E-mail.

Consome a API da AwesomeAPI para buscar a cotação do Dólar (USD-BRL)
e envia alertas via protocolo SMTP e pela Gmail API com OAuth 2.0.
"""

import base64
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def buscar_cotacao_dolar():
    """Consulta a API pública da AwesomeAPI e retorna o valor de compra."""
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    bid = dados["USDBRL"]["bid"]
    return bid


def enviar_email_smtp(cotacao):
    """Monta e envia e-mail via SMTP utilizando smtplib e email.mime."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    assunto = "Alerta de Cotação - Dólar Atualizado"
    corpo = (
        f"Olá,\n\nA cotação atual do Dólar (USD-BRL) é R$ {cotacao}.\n\n"
        "Notificação automática via RPA Bot."
    )

    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = assunto
    msg["From"] = remetente or "bot@exemplo.com"
    msg["To"] = destinatario or "usuario@exemplo.com"

    if not (remetente and senha_app and destinatario):
        print("[SMTP - MOCK] Variáveis de ambiente não configuradas.")
        print(f"[SMTP - MOCK] Para: {msg['To']} | Assunto: {msg['Subject']}")
        print(f"[SMTP - MOCK] Corpo:\n{corpo}")
        return True

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha_app)
        servidor.send_message(msg)

    print("[SMTP] E-mail enviado com sucesso!")
    return True


def enviar_email_gmail_api(cotacao):
    """Envia o e-mail pela Gmail API do Google com autenticação OAuth 2.0."""
    diretorio_base = Path(__file__).resolve().parent
    caminho_credenciais = diretorio_base / "credentials.json"
    caminho_token = diretorio_base / "token.json"

    assunto = "Alerta de Cotação - Gmail API"
    corpo = f"Cotação do Dólar capturada via API: R$ {cotacao}"

    msg = MIMEText(corpo, "plain", "utf-8")
    msg["Subject"] = assunto
    msg["To"] = os.getenv("EMAIL_DESTINATARIO", "usuario@exemplo.com")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

    if not caminho_credenciais.exists() and not caminho_token.exists():
        print("[Gmail API - MOCK] credentials.json não encontrado.")
        print(f"[Gmail API - MOCK] Para: {msg['To']} | Cotação: R$ {cotacao}")
        return True

    creds = None
    if caminho_token.exists():
        creds = Credentials.from_authorized_user_file(
            str(caminho_token), SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(
                str(caminho_credenciais), SCOPES
            )
            creds = fluxo.run_local_server(port=0)

        with open(caminho_token, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    servico = build("gmail", "v1", credentials=creds)
    mensagem = servico.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()
    print(f"[Gmail API] Mensagem enviada! ID: {mensagem.get('id')}")
    return True


def main():
    """Função orquestradora."""
    print("Buscando cotação do Dólar na AwesomeAPI...")
    cotacao = buscar_cotacao_dolar()
    print(f"Cotação encontrada: R$ {cotacao}")

    print("\n1. Testando envio via SMTP:")
    try:
        enviar_email_smtp(cotacao)
    except Exception as erro_smtp:
        print(f"[ERRO SMTP] Falha ao enviar via SMTP: {erro_smtp}")

    print("\n2. Testando envio via Gmail API:")
    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro_gmail:
        print(f"[ERRO Gmail API] Falha ao enviar via Gmail API: {erro_gmail}")


if __name__ == "__main__":
    main()
