"""
AULA 12 - Integração de Sistemas via APIs REST e Notificações E-mail

Bot que:
1. Consulta a cotação do Dólar via AwesomeAPI (GET JSON)
2. Envia alerta por e-mail via SMTP (smtplib)
3. Envia alerta por e-mail via Gmail API (OAuth 2.0)

Credenciais lidas de variáveis de ambiente:
  EMAIL_REMETENTE       - endereço do remetente
  EMAIL_SENHA_APP       - senha de app do Google (não a senha da conta)
  EMAIL_DESTINATARIO    - endereço do destinatário
  MOCK_EMAIL            - se 'true', imprime o e-mail no terminal em vez de enviar

Nunca commitar credentials.json nem token.json.
"""
from __future__ import annotations

import base64
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

# ---------------------------------------------------------------------------
# Configuração de logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    filename="app_rpa.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
URL_AWESOMEAPI = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


# ---------------------------------------------------------------------------
# 1. Consumo da API
# ---------------------------------------------------------------------------

def buscar_cotacao_dolar() -> str:
    """Consulta a AwesomeAPI e retorna o valor de compra (bid) do Dólar."""
    resposta = requests.get(URL_AWESOMEAPI, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    cotacao = dados["USDBRL"]["bid"]
    logger.info("Cotação USD/BRL obtida: %s", cotacao)
    return cotacao


# ---------------------------------------------------------------------------
# 2. Envio de e-mail via SMTP
# ---------------------------------------------------------------------------

def enviar_email_smtp(cotacao: str) -> None:
    """
    Monta e envia e-mail de alerta de cotação via SMTP (smtplib + starttls).

    Lê EMAIL_REMETENTE, EMAIL_SENHA_APP e EMAIL_DESTINATARIO do ambiente.
    Se MOCK_EMAIL='true', apenas imprime a mensagem (modo CI/mock).
    """
    remetente = os.getenv("EMAIL_REMETENTE", "remetente@exemplo.com")
    senha = os.getenv("EMAIL_SENHA_APP", "")
    destinatario = os.getenv("EMAIL_DESTINATARIO", remetente)
    mock = os.getenv("MOCK_EMAIL", "false").lower() == "true"

    # Monta a mensagem com email.mime
    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = f"Alerta de Cotação: USD/BRL = R$ {cotacao}"
    corpo = (
        f"Olá!\n\n"
        f"A cotação atual do Dólar é:\n"
        f"  Compra (bid): R$ {cotacao}\n\n"
        f"Enviado automaticamente pelo Bot de Cotação RPA.\n"
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    if mock:
        print("[SMTP MOCK] E-mail que seria enviado:")
        print(f"  Para: {destinatario}")
        print(f"  Assunto: {msg['Subject']}")
        print(f"  Corpo:\n{corpo}")
        logger.info("SMTP mock: e-mail impresso no terminal.")
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
        servidor.ehlo()
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
    logger.info("E-mail SMTP enviado para %s", destinatario)
    print(f"[SMTP] E-mail enviado para {destinatario}")


# ---------------------------------------------------------------------------
# 3. Envio de e-mail via Gmail API (OAuth 2.0)
# ---------------------------------------------------------------------------

def enviar_email_gmail_api(cotacao: str) -> None:
    """
    Monta e envia e-mail de alerta de cotação via Gmail API com OAuth 2.0.

    Usa escopo gmail.send e googleapiclient.
    Se MOCK_EMAIL='true', apenas imprime a mensagem (modo CI/mock).
    """
    from pathlib import Path

    mock = os.getenv("MOCK_EMAIL", "false").lower() == "true"
    destinatario = os.getenv("EMAIL_DESTINATARIO", "destinatario@exemplo.com")

    # Monta a mensagem com email.mime
    msg = MIMEMultipart()
    msg["To"] = destinatario
    msg["Subject"] = f"[Gmail API] Alerta de Cotação: USD/BRL = R$ {cotacao}"
    corpo = (
        f"Olá!\n\n"
        f"A cotação atual do Dólar (via Gmail API) é:\n"
        f"  Compra (bid): R$ {cotacao}\n\n"
        f"Enviado automaticamente pelo Bot de Cotação RPA.\n"
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    if mock:
        print("[GMAIL API MOCK] E-mail que seria enviado:")
        print(f"  Para: {destinatario}")
        print(f"  Assunto: {msg['Subject']}")
        print(f"  Corpo:\n{corpo}")
        logger.info("Gmail API mock: e-mail impresso no terminal.")
        return

    # Autenticação OAuth 2.0
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    pasta = Path(__file__).resolve().parent
    token_path = pasta / "token.json"
    credentials_path = pasta / "credentials.json"

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError(
                    f"credentials.json não encontrado em: {credentials_path}\n"
                    "Baixe do Google Cloud Console (OAuth 2.0 para Desktop)."
                )
            fluxo = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = fluxo.run_local_server(port=0)
        token_path.write_text(creds.to_json(), encoding="utf-8")

    service = build("gmail", "v1", credentials=creds)

    # Codifica em base64 URL-safe e envia via users().messages().send
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    resposta = service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()

    msg_id = resposta.get("id", "?")
    logger.info("E-mail Gmail API enviado para %s (id: %s)", destinatario, msg_id)
    print(f"[Gmail API] E-mail enviado para {destinatario} (id: {msg_id})")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Ponto de entrada: consulta cotação e tenta enviar por SMTP e Gmail API.
    Se MOCK_EMAIL='true', imprime no terminal em vez de enviar (modo CI).
    """
    print("=" * 60)
    print("Bot de Cotação e Alerta - AULA 12 RPA")
    print("=" * 60)

    # 1. Consulta a API
    try:
        cotacao = buscar_cotacao_dolar()
        print(f"Cotação USD/BRL (bid): R$ {cotacao}")
    except requests.RequestException as erro:
        logger.error("Erro ao consultar AwesomeAPI: %s", erro)
        print(f"[ERRO] Não foi possível consultar a API: {erro}")
        # Em modo mock/CI, usa um valor fictício para continuar
        cotacao = "5.00"
        print(f"[MOCK] Usando cotação fictícia: R$ {cotacao}")

    # 2. Envio via SMTP
    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:  # noqa: BLE001
        logger.error("Falha no envio SMTP: %s", erro)
        print(f"[ERRO SMTP] {erro}")

    # 3. Envio via Gmail API
    try:
        enviar_email_gmail_api(cotacao)
    except ImportError:
        msg = (
            "Instale as dependências da Gmail API:\n"
            "  pip install google-api-python-client "
            "google-auth-httplib2 google-auth-oauthlib"
        )
        logger.warning(msg)
        print(f"[AVISO] {msg}")
    except Exception as erro:  # noqa: BLE001
        logger.error("Falha no envio Gmail API: %s", erro)
        print(f"[ERRO Gmail API] {erro}")

    print("=" * 60)
    print("Bot finalizado.")


if __name__ == "__main__":
    main()
