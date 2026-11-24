import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from pathlib import Path
import smtplib
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

AWESOME_API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def buscar_cotacao_dolar() -> tuple[float, dict[str, Any]]:
    """Consulta a AwesomeAPI e retorna (bid_float, dados_usdbrl)."""
    response = requests.get(AWESOME_API_URL, timeout=10)
    response.raise_for_status()

    data = response.json()
    usd_brl = data.get("USDBRL")
    if not isinstance(usd_brl, dict) or "bid" not in usd_brl:
        raise ValueError("Estrutura JSON inválida: campo 'USDBRL.bid' ausente.")

    cotacao = float(usd_brl["bid"])
    return cotacao, usd_brl


def _montar_mensagem(
    cotacao: float,
    remetente: str,
    destinatario: str,
    canal: str,
    detalhes: dict[str, Any] | None = None,
) -> MIMEMultipart:
    """Monta mensagem MIME com versões texto puro (plain) e HTML."""
    detalhes = detalhes or {}
    alta = detalhes.get("high", "N/A")
    baixa = detalhes.get("low", "N/A")
    variacao = detalhes.get("pctChange", "N/A")
    atualizado_em = detalhes.get("create_date", "N/A")

    assunto = f"Alerta de Cotação — Dólar (USD/BRL): R$ {cotacao:.4f}"

    corpo_texto = (
        f"Cotação Atual do Dólar (USD/BRL)\n"
        f"Valor de compra (bid): R$ {cotacao:.4f}\n"
        f"Máxima: R$ {alta}\n"
        f"Mínima: R$ {baixa}\n"
        f"Variação (%): {variacao}%\n"
        f"Atualizado em: {atualizado_em}\n"
        f"Canal: {canal}\n"
    )

    corpo_html = f"""
    <html>
      <body>
        <h2>Alerta de Cotação — Dólar (USD/BRL)</h2>
        <p><strong>Valor de compra (bid):</strong> R$ {cotacao:.4f}</p>
        <ul>
          <li><strong>Máxima:</strong> R$ {alta}</li>
          <li><strong>Mínima:</strong> R$ {baixa}</li>
          <li><strong>Variação (%):</strong> {variacao}%</li>
          <li><strong>Atualizado em:</strong> {atualizado_em}</li>
        </ul>
        <p><small>Enviado via {canal}</small></p>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = destinatario

    msg.attach(MIMEText(corpo_texto, "plain", "utf-8"))
    msg.attach(MIMEText(corpo_html, "html", "utf-8"))
    return msg


def _imprimir_mock(canal: str, msg: MIMEMultipart) -> str:
    """Imprime o e-mail no terminal quando credenciais não estão configuradas."""
    texto_plain = ""
    for parte in msg.walk():
        if parte.get_content_type() == "text/plain":
            payload = parte.get_payload(decode=True) or b""
            charset = parte.get_content_charset() or "utf-8"
            texto_plain = payload.decode(charset, errors="replace")
            break

    print(f"\n[MOCK - {canal}] Credenciais não configuradas. Simulando envio:")
    print(f"De: {msg['From']}")
    print(f"Para: {msg['To']}")
    print(f"Assunto: {msg['Subject']}")
    print(texto_plain.strip())
    return f"Mock exibido no terminal ({canal})"


def enviar_email_smtp(
    cotacao: float, detalhes: dict[str, Any] | None = None
) -> str:
    """Envia notificação por e-mail via SMTP (STARTTLS) usando variáveis de ambiente."""
    remetente = os.getenv("EMAIL_REMETENTE", "").strip()
    senha_app = os.getenv("EMAIL_SENHA_APP", "").strip()
    destinatario = os.getenv("EMAIL_DESTINATARIO", "").strip()

    msg = _montar_mensagem(
        cotacao=cotacao,
        remetente=remetente or "remetente_mock@exemplo.com",
        destinatario=destinatario or "destinatario_mock@exemplo.com",
        canal="SMTP (smtp.gmail.com:587)",
        detalhes=detalhes,
    )

    if not remetente or not senha_app or not destinatario:
        return _imprimir_mock("SMTP", msg)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as servidor:
        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()
        servidor.login(remetente, senha_app)
        servidor.send_message(msg)

    return f"E-mail enviado via SMTP para {destinatario}"


def _obter_credenciais_gmail() -> Credentials | None:
    """Carrega, renova ou solicita autorização OAuth 2.0 para a Gmail API."""
    creds: Credentials | None = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), GMAIL_SCOPES
        )

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
        return creds

    if not CREDENTIALS_FILE.exists():
        return None

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CREDENTIALS_FILE), GMAIL_SCOPES
    )
    creds = flow.run_local_server(port=0)
    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return creds


def enviar_email_gmail_api(
    cotacao: float, detalhes: dict[str, Any] | None = None
) -> str:
    """Envia notificação por e-mail usando a Gmail API (users.messages.send)."""
    remetente = os.getenv("EMAIL_REMETENTE", "").strip() or "me"
    destinatario = (
        os.getenv("EMAIL_DESTINATARIO", "").strip()
        or "destinatario_mock@exemplo.com"
    )

    msg = _montar_mensagem(
        cotacao=cotacao,
        remetente=remetente,
        destinatario=destinatario,
        canal="Gmail API",
        detalhes=detalhes,
    )

    creds = _obter_credenciais_gmail()
    if creds is None:
        return _imprimir_mock("Gmail API", msg)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    service = build("gmail", "v1", credentials=creds)
    enviado = (
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
    )
    msg_id = enviado.get("id", "sem-id")
    return f"E-mail enviado via Gmail API (ID: {msg_id})"


def main() -> None:
    cotacao, detalhes = buscar_cotacao_dolar()
    print(f"Cotação atual do Dólar (bid): R$ {cotacao:.4f}")

    try:
        resultado_smtp = enviar_email_smtp(cotacao, detalhes)
        print(f"[SMTP] {resultado_smtp}")
    except Exception as exc:
        print(f"[SMTP] Erro no envio: {exc}")

    try:
        resultado_gmail = enviar_email_gmail_api(cotacao, detalhes)
        print(f"[Gmail API] {resultado_gmail}")
    except Exception as exc:
        print(f"[Gmail API] Erro no envio: {exc}")


if __name__ == "__main__":
    main()