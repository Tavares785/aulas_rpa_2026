import base64
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests


URL_COTACAO = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_PATH = BASE_DIR / "credentials.json"
TOKEN_PATH = BASE_DIR / "token.json"


def obter_cotacao_dolar() -> str:
    resposta = requests.get(URL_COTACAO, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    return str(dados["USDBRL"]["bid"])

def montar_mensagem_email(cotacao: str, remetente: str, destinatario: str) -> MIMEText:
    mensagem = MIMEText(f"Cotacao atual do Dolar (USD/BRL - compra): R$ {cotacao}", "plain", "utf-8")
    mensagem["Subject"] = "Alerta de Cotacao - USD/BRL"
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    return mensagem


def enviar_email_smtp(cotacao: str) -> str:
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not remetente or not senha_app or not destinatario:
        mensagem_mock = montar_mensagem_email(
            cotacao,
            remetente or "mock@exemplo.com",
            destinatario or "destino@exemplo.com",
        )
        print("[MOCK SMTP] Credenciais nao configuradas. E-mail simulado:")
        print(mensagem_mock.as_string())
        return "MOCK SMTP"

    mensagem = montar_mensagem_email(cotacao, remetente, destinatario)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha_app)
        servidor.send_message(mensagem)

    return "SMTP OK"

def obter_credenciais_gmail() -> Credentials | None:
    if not CREDENTIALS_PATH.exists():
        return None

    credenciais = None
    if TOKEN_PATH.exists():
        credenciais = Credentials.from_authorized_user_file(str(TOKEN_PATH), GMAIL_SCOPES)

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), GMAIL_SCOPES)
            credenciais = fluxo.run_local_server(port=0)

        TOKEN_PATH.write_text(credenciais.to_json(), encoding="utf-8")

    return credenciais


def enviar_email_gmail_api(cotacao: str) -> str:
    destinatario = os.getenv("EMAIL_DESTINATARIO") or "destino@exemplo.com"
    remetente = os.getenv("EMAIL_REMETENTE") or "me"
    mensagem = montar_mensagem_email(cotacao, remetente, destinatario)
    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode("utf-8")

    credenciais = obter_credenciais_gmail()
    if credenciais is None:
        print("[MOCK GMAIL API] credentials.json nao encontrado. E-mail simulado:")
        print(mensagem.as_string())
        return "MOCK GMAIL API"

    servico = build("gmail", "v1", credentials=credenciais)
    servico.users().messages().send(userId="me", body={"raw": raw}).execute()
    return "GMAIL API OK"

cotacao_dolar = obter_cotacao_dolar()
print(f"Cotacao USD/BRL: {cotacao_dolar}")

try:
    resultado_smtp = enviar_email_smtp(cotacao_dolar)
    print(f"Resultado SMTP: {resultado_smtp}")
except Exception as erro_smtp:
    print(f"Falha no envio SMTP: {erro_smtp}")

try:
    resultado_gmail = enviar_email_gmail_api(cotacao_dolar)
    print(f"Resultado Gmail API: {resultado_gmail}")
except Exception as erro_gmail:
    print(f"Falha no envio Gmail API: {erro_gmail}")