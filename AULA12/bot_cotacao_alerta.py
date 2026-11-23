"""
Lab 12 - Integração de Sistemas via APIs REST e Notificações E-mail
Script: bot_cotacao_alerta.py
RA: 6326327

Fluxo:
1. Consulta a cotação do Dólar na AwesomeAPI (GET JSON).
2. Extrai o campo 'bid' (valor de compra).
3. Envia alerta por e-mail via SMTP (smtplib + email.mime).
4. Envia o mesmo alerta via Gmail API (OAuth 2.0 + googleapiclient).

Credenciais lidas exclusivamente de variáveis de ambiente:
  EMAIL_REMETENTE       — endereço do remetente Gmail
  EMAIL_SENHA_APP       — Senha de App do Google (não a senha da conta)
  EMAIL_DESTINATARIO    — endereço do destinatário

Nunca commit credentials.json ou token.json.
Requer: pip install requests google-api-python-client
        google-auth-httplib2 google-auth-oauthlib
"""
from __future__ import annotations

import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

try:
    import requests
    REQUESTS_DISPONIVEL = True
except ImportError:
    requests = None  # type: ignore[assignment]
    REQUESTS_DISPONIVEL = False

try:
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    GOOGLE_DISPONIVEL = True
except ImportError:
    GOOGLE_DISPONIVEL = False

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------
URL_AWESOMEAPI = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA = Path(__file__).resolve().parent
CREDENCIAIS = PASTA / "credentials.json"
TOKEN = PASTA / "token.json"

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


# ---------------------------------------------------------------------------
# 1. Consulta de cotação
# ---------------------------------------------------------------------------
def buscar_cotacao() -> str:
    """Consulta a AwesomeAPI e retorna o valor 'bid' do Dólar."""
    resposta = requests.get(URL_AWESOMEAPI, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()
    bid = dados["USDBRL"]["bid"]
    return bid


# ---------------------------------------------------------------------------
# 2. Montagem da mensagem
# ---------------------------------------------------------------------------
def montar_mensagem(cotacao: str, remetente: str, destinatario: str) -> MIMEMultipart:
    """Monta o e-mail de alerta com email.mime."""
    corpo = (
        f"Alerta de Cotação — Dólar (USD/BRL)\n\n"
        f"Valor de compra (bid): R$ {cotacao}\n\n"
        f"Fonte: AwesomeAPI (economia.awesomeapi.com.br)"
    )
    msg = MIMEMultipart()
    msg["Subject"] = f"Alerta: Dólar a R$ {cotacao}"
    msg["From"] = remetente
    msg["To"] = destinatario
    msg.attach(MIMEText(corpo, _subtype="plain", _charset="utf-8"))
    return msg


# ---------------------------------------------------------------------------
# 3. Envio via SMTP
# ---------------------------------------------------------------------------
def enviar_email_smtp(cotacao: str) -> None:
    """Envia alerta de cotação via smtplib (STARTTLS, porta 587)."""
    remetente = os.getenv("EMAIL_REMETENTE", "")
    senha = os.getenv("EMAIL_SENHA_APP", "")
    destinatario = os.getenv("EMAIL_DESTINATARIO", remetente)

    msg = montar_mensagem(cotacao, remetente, destinatario)

    # Sem credenciais configuradas: modo mock (imprime no terminal).
    if not remetente or not senha:
        print("[SMTP MOCK] Credenciais não configuradas — e-mail simulado:")
        print(f"  Assunto : {msg['Subject']}")
        print(f"  Para    : {msg['To']}")
        return

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
        servidor.ehlo()
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.sendmail(remetente, destinatario, msg.as_string())
    print(f"[SMTP] E-mail enviado para {destinatario}.")


# ---------------------------------------------------------------------------
# 4. Envio via Gmail API (OAuth 2.0)
# ---------------------------------------------------------------------------
def _obter_servico_gmail():
    """Autentica via OAuth2 (reutiliza/renova token.json) e retorna o cliente."""
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENCIAIS.exists():
                raise FileNotFoundError(
                    f"credentials.json não encontrado em {PASTA}. "
                    "Baixe no Google Cloud Console e não faça commit do arquivo."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENCIAIS), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
    return build("gmail", "v1", credentials=creds)


def enviar_email_gmail_api(cotacao: str) -> None:
    """Envia alerta de cotação via Gmail API com autenticação OAuth 2.0."""
    if not GOOGLE_DISPONIVEL:
        print(
            "[Gmail API] Dependências ausentes. Instale com:\n"
            "  pip install google-api-python-client "
            "google-auth-httplib2 google-auth-oauthlib"
        )
        return

    remetente = os.getenv("EMAIL_REMETENTE", "me")
    destinatario = os.getenv("EMAIL_DESTINATARIO", remetente)
    msg = montar_mensagem(cotacao, remetente, destinatario)

    # Sem credentials.json: modo mock.
    if not CREDENCIAIS.exists():
        print("[Gmail API MOCK] credentials.json ausente — e-mail simulado:")
        print(f"  Assunto : {msg['Subject']}")
        print(f"  Para    : {msg['To']}")
        return

    servico = _obter_servico_gmail()
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    resultado = servico.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()
    print(f"[Gmail API] E-mail enviado. ID da mensagem: {resultado['id']}")


# ---------------------------------------------------------------------------
# 5. Execução principal
# ---------------------------------------------------------------------------
def main() -> None:
    if not REQUESTS_DISPONIVEL:
        print("requests não instalado. Rode: pip install requests")
        raise SystemExit(0)

    # Busca cotação
    try:
        cotacao = buscar_cotacao()
        print(f"Cotação USD/BRL (bid): R$ {cotacao}")
    except Exception as erro:  # noqa: BLE001
        print(f"Não foi possível buscar a cotação: {erro}")
        raise SystemExit(0)

    # Envio SMTP — falha não impede a tentativa via Gmail API
    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:  # noqa: BLE001
        print(f"[SMTP] Falha no envio: {erro}")

    # Envio Gmail API — independente do SMTP
    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro:  # noqa: BLE001
        print(f"[Gmail API] Falha no envio: {erro}")


if __name__ == "__main__":
    main()
