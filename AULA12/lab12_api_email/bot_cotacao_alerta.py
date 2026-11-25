import requests
from email.mime.text import MIMEText
import os
import smtplib
from email.mime.multipart import MIMEMultipart
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send"
]


def autenticar_gmail():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "AULA12/lab12_api_email/credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

def obter_cotacao_dolar():

    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    resposta = requests.get(url)

    dados = resposta.json()

    cotacao = dados["USDBRL"]["bid"]

    return cotacao


def enviar_email_smtp(cotacao):

    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not remetente:
        print("Modo Mock SMTP")
        print(f"Cotação: R$ {cotacao}")
        return

    mensagem = MIMEMultipart()

    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = "Cotação do Dólar"

    texto = f"""
    Olá,

    O dólar está em:

    R$ {cotacao}

    Mensagem automática.
    """

    mensagem.attach(MIMEText(texto, "plain"))

    servidor = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    servidor.starttls()

    servidor.login(
        remetente,
        senha
    )

    servidor.send_message(mensagem)

    servidor.quit()

    print("Email enviado por SMTP")

def enviar_email_gmail_api(cotacao):

    if not os.path.exists("AULA12/lab12_api_email/credentials.json"):

        print("\n[MOCK GMAIL API]")
        print(f"Cotação atual do dólar: R$ {cotacao}")

        return

    creds = autenticar_gmail()

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    mensagem = MIMEText(
        f"Cotação atual do dólar: R$ {cotacao}"
    )

    mensagem["to"] = os.getenv(
        "EMAIL_DESTINATARIO",
        "teste@gmail.com"
    )

    mensagem["subject"] = "Alerta de Cotação"

    raw = base64.urlsafe_b64encode(
        mensagem.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    print("Email enviado via Gmail API")

    
def main():

    cotacao = obter_cotacao_dolar()

    print(f"Cotação atual: R$ {cotacao}")

    try:
        enviar_email_smtp(cotacao)

    except Exception as erro:
        print(f"Erro SMTP: {erro}")

    try:
        enviar_email_gmail_api(cotacao)

    except Exception as erro:
        print(f"Erro Gmail API: {erro}")


if __name__ == "__main__":
    main()