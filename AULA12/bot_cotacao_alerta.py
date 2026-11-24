import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import os
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

def enviar_gmail_email_api(cotacao):
    user.