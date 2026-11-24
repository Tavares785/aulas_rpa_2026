import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests


API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def obter_cotacao_dolar() -> float:
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    dados = response.json()
    cotacao_str = dados["USDBRL"]["bid"]
    return float(cotacao_str)


def montar_mensagem(
    remetente: str, destinatario: str, cotacao: float, canal: str
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Alerta de Cotacao USD/BRL: R$ {cotacao:.4f}"
    msg["From"] = remetente
    msg["To"] = destinatario

    texto_simples = (
        f"Cotacao atual do Dolar (USD-BRL): R$ {cotacao:.4f}\n"
        f"Canal de envio: {canal}\n"
        f"Fonte: AwesomeAPI ({API_URL})"
    )

    corpo_html = f"""
    <html>
      <body>
        <h2>Alerta de Cotacao - USD/BRL</h2>
        <p><strong>Valor de compra (bid):</strong> R$ {cotacao:.4f}</p>
        <p><strong>Canal:</strong> {canal}</p>
        <p><small>Fonte: AwesomeAPI</small></p>
      </body>
    </html>
    """

    msg.attach(MIMEText(texto_simples, "plain", "utf-8"))
    msg.attach(MIMEText(corpo_html, "html", "utf-8"))
    return msg


def enviar_email_smtp(cotacao: float) -> bool:
    remetente = os.getenv("EMAIL_REMETENTE", "").strip()
    senha_app = os.getenv("EMAIL_SENHA_APP", "").strip()
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()

    if not remetente or not senha_app or not destinatario:
        print("[MOCK SMTP] Credenciais de ambiente nao configuradas.")
        print(f"[MOCK SMTP] Para: {destinatario or 'nao_definido'} | Assunto: Alerta USD/BRL R$ {cotacao:.4f}")
        print(f"[MOCK SMTP] Cotacao USD-BRL extraida: R$ {cotacao:.4f}")
        return False

    mensagem = montar_mensagem(remetente, destinatario, cotacao, "SMTP")

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(remetente, senha_app)
        server.sendmail(remetente, [destinatario], mensagem.as_string())

    print(f"[SMTP] E-mail enviado com sucesso para {destinatario} (USD/BRL: R$ {cotacao:.4f}).")
    return True


def obter_credenciais_gmail() -> Credentials | None:
    if not CREDENTIALS_FILE.exists():
        return None

    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), GMAIL_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), GMAIL_SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return creds


def enviar_email_gmail_api(cotacao: float) -> bool:
    creds = obter_credenciais_gmail()
    remetente = os.getenv("EMAIL_REMETENTE", "me").strip() or "me"
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()

    if creds is None or not destinatario:
        print("[MOCK GMAIL API] credentials.json ou EMAIL_DESTINATARIO nao configurado.")
        print(f"[MOCK GMAIL API] Para: {destinatario or 'nao_definido'} | Assunto: Alerta USD/BRL R$ {cotacao:.4f}")
        print(f"[MOCK GMAIL API] Cotacao USD-BRL extraida: R$ {cotacao:.4f}")
        return False

    mensagem = montar_mensagem(remetente, destinatario, cotacao, "Gmail API")
    raw_bytes = base64.urlsafe_b64encode(mensagem.as_bytes())
    raw_str = raw_bytes.decode("utf-8")

    service = build("gmail", "v1", credentials=creds)
    resultado = (
        service.users()
        .messages()
        .send(userId="me", body={"raw": raw_str})
        .execute()
    )

    msg_id = resultado.get("id", "sem-id")
    print(f"[GMAIL API] E-mail enviado com sucesso (ID: {msg_id}, USD/BRL: R$ {cotacao:.4f}).")
    return True


def main() -> None:
    try:
        cotacao = obter_cotacao_dolar()
        print(f"[API] Cotacao atual USD-BRL (bid): R$ {cotacao:.4f}")
    except Exception as exc:
        print(f"[ERRO API] Falha ao obter cotacao do Dolar: {exc}")
        return

    try:
        enviar_email_smtp(cotacao)
    except Exception as exc:
        print(f"[ERRO SMTP] Falha ao enviar e-mail via SMTP: {exc}")

    try:
        enviar_email_gmail_api(cotacao)
    except Exception as exc:
        print(f"[ERRO GMAIL API] Falha ao enviar e-mail via Gmail API: {exc}")


if __name__ == "__main__":
    main()