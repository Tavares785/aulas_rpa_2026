import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import os

# impotacao google
import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
site = requests.get(url)
resposta = site.json()
cotacao = resposta.get('USDBRL',{}).get('bid')


def enviar_email_smtp(cotacao):
    server_smpt = "smtp.gmail.com"
    port = 587
    sender_email = os.getenv("EMAIL_DESTINATARIO")
    password = os.getenv("EMAIL_SENHA_APP")

    receive_email = os.getenv("EMAIL_REMETENTE")
    subject = "Cotacao Dolar Atual"
    body = f"cotacao atual: {cotacao}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receive_email
    message["Subject"] = subject
    message.attach(MIMEText(body, plain))

def validar_JSON():
    SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    # valida o token JSON e credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        return creds


def enviar_gmail_email_api(cotacao):
    # envio do email
    service = build("gmail", "v1", credentials=autenticar())

    receive_email = os.getenv("EMAIL_REMETENTE")
    subject = "Cotacao Dolar Atual"
    body = f"cotacao atual: {cotacao}"

    msg = EmailMessage()
    msg.set_content(body)
    msg["To"] = receive_email
    msg["Subject"] = body

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    resposta = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("Email enviado! ID:", resposta["id"])
