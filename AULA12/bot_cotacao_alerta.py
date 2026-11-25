"""
Lab 12 - APIs REST e notificacao por e-mail (SMTP e Gmail API)
RA: 6326012

Busca a cotacao do dolar na AwesomeAPI e manda um e-mail com o valor
de duas formas: pelo SMTP do Gmail e pela Gmail API.
Se as credenciais nao estiverem configuradas, o e-mail e so mostrado
no terminal (mock).
"""
import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA = Path(__file__).parent
CREDENCIAIS = PASTA / "credentials.json"
TOKEN = PASTA / "token.json"


def buscar_cotacao():
    resposta = requests.get(URL_COTACAO, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


def montar_email(cotacao, remetente, destinatario):
    msg = MIMEMultipart()
    msg["Subject"] = f"Cotacao do dolar: R$ {cotacao:.4f}"
    msg["From"] = remetente
    msg["To"] = destinatario
    corpo = f"Ola!\n\nA cotacao atual do dolar (compra) e R$ {cotacao:.4f}.\n\nEnviado pelo bot de cotacao."
    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    return msg


def mostrar_mock(titulo, msg):
    print(f"[MOCK {titulo}] credenciais nao configuradas, e-mail que seria enviado:")
    print(f"  Para: {msg['To']}")
    print(f"  Assunto: {msg['Subject']}")
    print("  " + msg.get_payload()[0].get_payload(decode=True).decode("utf-8").replace("\n", "\n  "))


def enviar_email_smtp(cotacao):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    msg = montar_email(cotacao, remetente or "remetente@exemplo.com", destinatario or "destinatario@exemplo.com")

    if not (remetente and senha and destinatario):
        mostrar_mock("SMTP", msg)
        return

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)
    print("SMTP: e-mail enviado com sucesso")


def obter_servico_gmail():
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
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENCIAIS), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def enviar_email_gmail_api(cotacao):
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    msg = montar_email(cotacao, "me", destinatario or "destinatario@exemplo.com")

    if not (destinatario and CREDENCIAIS.exists()):
        mostrar_mock("Gmail API", msg)
        return

    service = obter_servico_gmail()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("Gmail API: e-mail enviado com sucesso")


def main():
    cotacao = buscar_cotacao()
    print(f"Cotacao atual do dolar (bid): R$ {cotacao:.4f}\n")

    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:
        print(f"SMTP: falha no envio -> {erro}")

    print()

    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro:
        print(f"Gmail API: falha no envio -> {erro}")


if __name__ == "__main__":
    main()
