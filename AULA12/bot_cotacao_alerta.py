"""Lab 12 - Integração via API REST e notificações por e-mail (SMTP e Gmail API).

Variáveis de ambiente (SMTP):
    EMAIL_REMETENTE, EMAIL_SENHA_APP, EMAIL_DESTINATARIO
Gmail API:
    credentials.json (OAuth 2.0 - app para computador) na pasta do script;
    token.json é gerado na primeira autenticação.
"""
import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def obter_cotacao() -> float:
    """Consulta a AwesomeAPI e devolve o valor de compra (bid) do dólar."""
    resposta = requests.get(URL_API, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


def montar_mensagem(cotacao: float, remetente: str, destinatario: str) -> MIMEMultipart:
    """Monta o e-mail com email.mime (usado pelos dois métodos de envio)."""
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = f"Alerta de cotação: Dólar a R$ {cotacao:.2f}"
    corpo = (
        "Olá!\n\n"
        f"A cotação atual de compra do Dólar (USD-BRL) é R$ {cotacao:.4f}.\n\n"
        "Mensagem automática - Lab 12."
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    return msg


def _imprimir_mock(metodo: str, msg: MIMEMultipart) -> None:
    print(f"[MOCK {metodo}] Credenciais não configuradas. E-mail que seria enviado:")
    print(f"  De: {msg['From']}")
    print(f"  Para: {msg['To']}")
    print(f"  Assunto: {msg['Subject']}")
    print(f"  Corpo: {msg.get_payload()[0].get_payload(decode=True).decode('utf-8')}")


def enviar_email_smtp(cotacao: float) -> None:
    """Envia o e-mail via SMTP (Gmail, porta 587, STARTTLS, Senha de App)."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    msg = montar_mensagem(cotacao, remetente or "remetente@exemplo.com",
                          destinatario or "destinatario@exemplo.com")

    if not (remetente and senha and destinatario):
        _imprimir_mock("SMTP", msg)
        return

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(msg)
    print("[SMTP] E-mail enviado com sucesso.")


def _autenticar_gmail():
    """Autentica via OAuth 2.0 (InstalledAppFlow) e devolve o serviço da Gmail API."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = fluxo.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def enviar_email_gmail_api(cotacao: float) -> None:
    """Envia o e-mail pela Gmail API (users.messages.send)."""
    remetente = os.getenv("EMAIL_REMETENTE", "me")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    msg = montar_mensagem(cotacao, remetente, destinatario or "destinatario@exemplo.com")

    if not (destinatario and os.path.exists(CREDENTIALS_FILE)):
        _imprimir_mock("GMAIL API", msg)
        return

    service = _autenticar_gmail()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("[GMAIL API] E-mail enviado com sucesso.")


def main() -> None:
    try:
        cotacao = obter_cotacao()
    except Exception as erro:
        print(f"[API] Falha ao obter a cotação: {erro}")
        return
    print(f"[API] Dólar (bid): R$ {cotacao:.4f}")

    # Cada envio é tratado separadamente: a falha de um não impede o outro.
    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:
        print(f"[SMTP] Falha no envio: {erro}")

    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro:
        print(f"[GMAIL API] Falha no envio: {erro}")


if __name__ == "__main__":
    main()