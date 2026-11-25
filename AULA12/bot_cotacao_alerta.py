"""
TF 12
"""
from __future__ import annotations

import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

URL_COTACAO_USD = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
TIMEOUT_SEGUNDOS = 15

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
PASTA_ATUAL = Path(__file__).resolve().parent
CREDENCIAIS_GMAIL = Path(
    os.getenv("GOOGLE_CREDENTIALS_FILE", PASTA_ATUAL / "credentials.json")
)
TOKEN_GMAIL = Path(
    os.getenv("GOOGLE_TOKEN_FILE", PASTA_ATUAL / "token.json")
)


def consultar_cotacao_dolar() -> float:
    """Consulta a AwesomeAPI e retorna o valor de compra (bid) do Dolar."""
    resposta = requests.get(URL_COTACAO_USD, timeout=TIMEOUT_SEGUNDOS)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


def montar_email_cotacao(
    cotacao: float, destinatario: str, remetente: str = ""
) -> MIMEMultipart:
    """Monta a mensagem MIME formatada com a cotacao atual do Dolar."""
    corpo = (
        "Alerta automatico de cotacao (AwesomeAPI)\n\n"
        f"Dolar Comercial (USD/BRL - compra/bid): R$ {cotacao:.4f}\n"
    )
    msg = MIMEMultipart()
    msg["Subject"] = f"Alerta de Cotacao USD/BRL: R$ {cotacao:.4f}"
    msg["To"] = destinatario
    if remetente:
        msg["From"] = remetente
    msg.attach(MIMEText(corpo, _subtype="plain", _charset="utf-8"))
    return msg


def exibir_email_mock(metodo: str, msg: MIMEMultipart) -> None:
    """Imprime o e-mail no terminal quando credenciais nao estao configuradas."""
    print(f"[MOCK - {metodo}] Credenciais ausentes; e-mail nao enviado:")
    print(f"  De     : {msg.get('From', '(conta autenticada)')}")
    print(f"  Para   : {msg['To']}")
    print(f"  Assunto: {msg['Subject']}")
    print("  Corpo  :")
    for parte in msg.get_payload():
        conteudo = parte.get_payload(decode=True).decode("utf-8", errors="replace")
        print(conteudo.strip())


def enviar_email_smtp(cotacao: float) -> str:
    """Envia alerta de cotacao via protocolo SMTP com STARTTLS."""
    remetente = os.getenv("EMAIL_REMETENTE", "").strip()
    senha_app = os.getenv("EMAIL_SENHA_APP", "").strip()
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()

    if not (remetente and senha_app and destinatario):
        msg_mock = montar_email_cotacao(
            cotacao,
            destinatario=destinatario or "destinatario@exemplo.com",
            remetente=remetente or "remetente@exemplo.com",
        )
        exibir_email_mock("SMTP", msg_mock)
        return "Modo mock executado (defina EMAIL_REMETENTE, EMAIL_SENHA_APP e EMAIL_DESTINATARIO)."

    msg = montar_email_cotacao(cotacao, destinatario=destinatario, remetente=remetente)
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=TIMEOUT_SEGUNDOS) as servidor:
        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()
        servidor.login(remetente, senha_app)
        servidor.send_message(msg)

    return f"E-mail enviado via SMTP para {destinatario}."


def carregar_credenciais_gmail():
    """Carrega, renova ou gera credenciais OAuth 2.0 para a Gmail API."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    creds = None
    if TOKEN_GMAIL.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_GMAIL), SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        fluxo = InstalledAppFlow.from_client_secrets_file(
            str(CREDENCIAIS_GMAIL), SCOPES
        )
        creds = fluxo.run_local_server(port=0)

    TOKEN_GMAIL.write_text(creds.to_json(), encoding="utf-8")
    TOKEN_GMAIL.chmod(0o600)
    return creds


def enviar_email_gmail_api(cotacao: float) -> str:
    """Envia alerta de cotacao pela Gmail API (users.messages.send)."""
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()

    if not TOKEN_GMAIL.exists() and not CREDENCIAIS_GMAIL.exists():
        msg_mock = montar_email_cotacao(
            cotacao, destinatario=destinatario or "(sua conta Gmail)"
        )
        exibir_email_mock("Gmail API", msg_mock)
        return "Modo mock executado (credentials.json/token.json nao encontrados)."

    from googleapiclient.discovery import build

    creds = carregar_credenciais_gmail()
    service = build("gmail", "v1", credentials=creds)

    if not destinatario:
        perfil = service.users().getProfile(userId="me").execute()
        destinatario = perfil["emailAddress"]

    msg = montar_email_cotacao(cotacao, destinatario=destinatario)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    resposta = service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()

    return f"E-mail enviado via Gmail API para {destinatario} (id: {resposta['id']})."


def main() -> int:
    """Orquestra a consulta da cotacao e os envios independentes por SMTP e Gmail API."""
    try:
        cotacao = consultar_cotacao_dolar()
    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"[ERRO] Falha ao obter cotacao do Dolar: {erro}")
        return 1

    print(f"Cotacao atual USD/BRL (bid): R$ {cotacao:.4f}\n")

    try:
        resultado_smtp = enviar_email_smtp(cotacao)
        print(f"[SMTP] {resultado_smtp}\n")
    except Exception as erro:
        print(f"[SMTP] Falha no envio: {erro}\n")

    try:
        resultado_gmail = enviar_email_gmail_api(cotacao)
        print(f"[Gmail API] {resultado_gmail}")
    except Exception as erro:
        print(f"[Gmail API] Falha no envio: {erro}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
