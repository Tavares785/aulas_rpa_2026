import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"


def obter_cotacao_dolar():
    """Consulta a AwesomeAPI e retorna o valor de compra (bid) do Dólar."""
    resposta = requests.get(URL_COTACAO, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


def montar_mensagem(cotacao, remetente, destinatario):
    """Cria o objeto MIMEMultipart formatado com o alerta de cotação."""
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = f"Alerta de Cotação USD/BRL: R$ {cotacao:.4f}"

    corpo = (
        f"Olá,\n\n"
        f"A cotação atual de compra (bid) do Dólar (USD-BRL) é R$ {cotacao:.4f}.\n\n"
        f"Mensagem enviada automaticamente pelo bot_cotacao_alerta.py."
    )
    mensagem.attach(MIMEText(corpo, "plain", "utf-8"))
    return mensagem


def enviar_email_smtp(cotacao):
    """Envia a cotação por e-mail utilizando servidor SMTP com STARTTLS."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not all([remetente, senha_app, destinatario]):
        remetente_mock = remetente or "remetente@exemplo.com"
        destinatario_mock = destinatario or "destinatario@exemplo.com"
        msg_mock = montar_mensagem(cotacao, remetente_mock, destinatario_mock)
        print("[SMTP - MOCK] Credenciais não configuradas nas variáveis de ambiente.")
        print(f"De: {msg_mock['From']} | Para: {msg_mock['To']} | Assunto: {msg_mock['Subject']}")
        return

    mensagem = montar_mensagem(cotacao, remetente, destinatario)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()
        servidor.login(remetente, senha_app)
        servidor.send_message(mensagem)

    print("[SMTP] E-mail enviado com sucesso!")


def enviar_email_gmail_api(cotacao):
    """Envia a cotação por e-mail utilizando a Gmail API (OAuth 2.0)."""
    remetente = os.getenv("EMAIL_REMETENTE", "me")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not os.path.exists("credentials.json") or not destinatario:
        destinatario_mock = destinatario or "destinatario@exemplo.com"
        msg_mock = montar_mensagem(cotacao, remetente, destinatario_mock)
        print("[Gmail API - MOCK] Arquivo credentials.json ou EMAIL_DESTINATARIO ausente.")
        print(f"De: {msg_mock['From']} | Para: {msg_mock['To']} | Assunto: {msg_mock['Subject']}")
        return

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    mensagem = montar_mensagem(cotacao, remetente, destinatario)
    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode("utf-8")

    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("[Gmail API] E-mail enviado com sucesso!")


def main():
    try:
        cotacao = obter_cotacao_dolar()
        print(f"Cotação atual USD-BRL (bid): R$ {cotacao:.4f}\n")
    except Exception as erro:
        print(f"[ERRO] Falha ao obter cotação da AwesomeAPI: {erro}")
        return

    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:
        print(f"[ERRO SMTP] Falha ao enviar e-mail via SMTP: {erro}")

    print("-" * 50)

    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro:
        print(f"[ERRO Gmail API] Falha ao enviar e-mail via Gmail API: {erro}")


if __name__ == "__main__":
    main()

