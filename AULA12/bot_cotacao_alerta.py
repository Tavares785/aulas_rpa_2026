"""
Bot de Cotação e Alerta por E-mail (SMTP e Gmail API).

Consome a API da AwesomeAPI para obter a cotação do Dólar e realiza o disparo
de alertas via SMTP e Gmail API (OAuth 2.0).
"""

import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    build = None
    InstalledAppFlow = None
    Request = None
    Credentials = None

# Escopos da API do Gmail necessários para envio de mensagens
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def obter_cotacao_dolar() -> str:
    """
    Acessa a API pública da AwesomeAPI e extrai o valor de compra (bid).

    URL: https://economia.awesomeapi.com.br/json/last/USD-BRL
    """
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    dados = response.json()
    cotacao = dados["USDBRL"]["bid"]
    return cotacao


def enviar_email_smtp(cotacao: str) -> None:
    """
    Monta e envia e-mail com a cotação utilizando smtplib e email.mime.

    Lê credenciais das variáveis de ambiente:
    - EMAIL_REMETENTE
    - EMAIL_SENHA_APP
    - EMAIL_DESTINATARIO

    Caso as credenciais não estejam configuradas, imprime no terminal (mock).
    """
    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    origem = remetente if remetente else "remetente.mock@exemplo.com"
    destino = destinatario if destinatario else "destinatario.mock@exemplo.com"

    msg = MIMEMultipart()
    msg["From"] = origem
    msg["To"] = destino
    msg["Subject"] = f"Alerta de Cotação: Dólar a R$ {cotacao}"

    corpo = (
        f"Olá,\n\n"
        f"A cotação atual de compra do Dólar (USD-BRL) é de R$ {cotacao}.\n\n"
        f"Notificação gerada automaticamente via SMTP.\n"
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    if not all([remetente, senha, destinatario]):
        print(
            "[SMTP] Credenciais não configuradas "
            "(EMAIL_REMETENTE, EMAIL_SENHA_APP, EMAIL_DESTINATARIO)."
        )
        print("[SMTP] Executando em modo MOCK. Detalhes do e-mail:")
        print("-------------------- MOCK E-MAIL SMTP --------------------")
        print(f"De: {msg['From']}")
        print(f"Para: {msg['To']}")
        print(f"Assunto: {msg['Subject']}")
        print(f"Corpo:\n{corpo.strip()}")
        print("----------------------------------------------------------")
        return

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)

    print(f"[SMTP] E-mail enviado com sucesso para {destinatario}!")


def enviar_email_gmail_api(cotacao: str) -> None:
    """
    Envia e-mail com a cotação através da Gmail API (users.messages.send).

    Utiliza OAuth 2.0 com escopo https://www.googleapis.com/auth/gmail.send.
    Se credentials.json não existir, imprime o e-mail no terminal como mock.
    """
    remetente = os.getenv("EMAIL_REMETENTE", "me")
    destinatario = os.getenv(
        "EMAIL_DESTINATARIO", "destinatario.mock@exemplo.com"
    )

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = destinatario
    msg["Subject"] = f"Alerta de Cotação (Gmail API): Dólar a R$ {cotacao}"

    corpo = (
        f"Olá,\n\n"
        f"A cotação atual de compra do Dólar (USD-BRL) é de R$ {cotacao}.\n\n"
        f"Notificação gerada automaticamente via Gmail API (OAuth 2.0).\n"
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

    credentials_path = "credentials.json"
    token_path = "token.json"

    credenciais_ausentes = (
        not os.path.exists(credentials_path) and not os.path.exists(token_path)
    )

    if build is None or credenciais_ausentes:
        print(
            "[Gmail API] Dependências ou credenciais não encontradas. "
            "Executando em modo MOCK."
        )
        print("------------------ MOCK E-MAIL GMAIL API ------------------")
        print(f"De: {msg['From']}")
        print(f"Para: {msg['To']}")
        print(f"Assunto: {msg['Subject']}")
        print(f"Corpo:\n{corpo.strip()}")
        print(f"Raw Base64 (preview): {raw[:50]}...")
        print("-----------------------------------------------------------")
        return

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    print("[Gmail API] E-mail enviado com sucesso via Gmail API!")


def main() -> None:
    """Executa o fluxo completo do bot integrador."""
    print("=== Iniciando Bot de Cotação e Alerta ===")

    try:
        cotacao = obter_cotacao_dolar()
        print(f"Cotação do Dólar obtida com sucesso: R$ {cotacao}")
    except Exception as e:
        print(
            f"Aviso: Não foi possível obter cotação ({e}). "
            "Usando valor padrão para teste."
        )
        cotacao = "5.50"

    print("\n[Passo 1] Notificação por E-mail via SMTP:")
    try:
        enviar_email_smtp(cotacao)
    except Exception as e:
        print(f"[SMTP] Falha no envio: {e}")

    print("\n[Passo 2] Notificação por E-mail via Gmail API:")
    try:
        enviar_email_gmail_api(cotacao)
    except Exception as e:
        print(f"[Gmail API] Falha no envio: {e}")

    print("\n=== Execução concluída ===")


if __name__ == "__main__":
    main()
