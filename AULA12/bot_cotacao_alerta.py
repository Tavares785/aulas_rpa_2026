import requests
import smtplib
import os
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def buscar_cotacao():

    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()

    dados = resposta.json()

    cotacao = dados["USDBRL"]["bid"]

    return float(cotacao)


def criar_mensagem(cotacao):

    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    assunto = "Alerta de Cotação do Dólar"

    corpo = f"""
Olá!

A cotação atual do dólar é:

R$ {cotacao:.2f}

Mensagem enviada automaticamente pelo Bot de Cotação.
"""

    mensagem = MIMEMultipart()

    if remetente:
        mensagem["From"] = remetente

    mensagem["To"] = destinatario or "destinatario@example.com"
    mensagem["Subject"] = assunto

    mensagem.attach(MIMEText(corpo, "plain", "utf-8"))

    return mensagem


def enviar_email_smtp(cotacao):

    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    mensagem = criar_mensagem(cotacao)

    if not remetente or not senha or not destinatario:
        print("\n[MOCK SMTP] Credenciais não configuradas.")
        print(mensagem.as_string())
        return

    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)

    print("E-mail enviado com sucesso via SMTP!")


def enviar_email_gmail_api(cotacao):

    mensagem = criar_mensagem(cotacao)

    if not os.path.exists("credentials.json"):
        print("\n[MOCK GMAIL API] Arquivo credentials.json não encontrado.")
        print(mensagem.as_string())
        return

    if not os.getenv("EMAIL_DESTINATARIO"):
        print("\n[MOCK GMAIL API] Destinatário não configurado.")
        print(mensagem.as_string())
        return

    credenciais = None

    if os.path.exists("token.json"):
        credenciais = Credentials.from_authorized_user_file(
            "token.json", SCOPES
        )

    if credenciais and credenciais.expired and credenciais.refresh_token:
        credenciais.refresh(Request())

    elif not credenciais or not credenciais.valid:
        fluxo = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )

        credenciais = fluxo.run_local_server(port=0)

    with open("token.json", "w", encoding="utf-8") as arquivo:
        arquivo.write(credenciais.to_json())

    servico = build("gmail", "v1", credentials=credenciais)

    mensagem_bytes = mensagem.as_bytes()

    mensagem_codificada = base64.urlsafe_b64encode(
        mensagem_bytes
    ).decode("utf-8")

    resultado = servico.users().messages().send(
        userId="me",
        body={"raw": mensagem_codificada}
    ).execute()

    print("E-mail enviado com sucesso via Gmail API!")
    print(f"ID da mensagem: {resultado['id']}")


def main():
    print("Iniciando consulta da cotação...")

    try:
        cotacao = buscar_cotacao()
        print(f"Cotação atual do dólar: R$ {cotacao:.2f}")

    except requests.exceptions.RequestException as erro:
        print(f"Erro ao consultar a API: {erro}")
        return

    except (KeyError, ValueError) as erro:
        print(f"Erro ao processar os dados da cotação: {erro}")
        return

    try:
        enviar_email_smtp(cotacao)

    except Exception as erro:
        print(f"Erro no envio SMTP: {erro}")

    try:
        print("\nIniciando envio pela Gmail API")
        enviar_email_gmail_api(cotacao)

    except Exception as erro:
        print(f"Erro no envio pela Gmail API: {erro}")


if __name__ == "__main__":
    main()
