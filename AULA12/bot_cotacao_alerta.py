"""
Lab 12 - Integração de Sistemas via APIs REST e Notificações por E-mail
Aluno: Icaro Ferrari de Senço - RA 1926102

Fluxo:
1. Consulta a cotação do Dólar na AwesomeAPI (GET + JSON).
2. Extrai o valor de compra ("bid").
3. Envia um alerta por e-mail via SMTP (smtplib + email.mime).
4. Envia o mesmo alerta via Gmail API (OAuth 2.0 + users.messages.send).

Credenciais NUNCA ficam no código:
- SMTP: variáveis de ambiente EMAIL_REMETENTE, EMAIL_SENHA_APP, EMAIL_DESTINATARIO.
- Gmail API: arquivos credentials.json / token.json (listados no .gitignore).
Se algo não estiver configurado, o e-mail é impresso no terminal (mock).
"""

import base64
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORTA = 587
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(PASTA, "credentials.json")
TOKEN_FILE = os.path.join(PASTA, "token.json")


# ---------------------------------------------------------------------------
# 1 e 2 - Consumo da API e processamento do JSON
# ---------------------------------------------------------------------------
def buscar_cotacao_dolar():
    """Faz GET na AwesomeAPI e devolve o valor de compra (bid) como float."""
    resposta = requests.get(URL_API, timeout=10)
    resposta.raise_for_status()  # erro HTTP (404, 500...) vira exceção
    dados = resposta.json()      # JSON -> dicionário Python
    # Estrutura: {"USDBRL": {"bid": "5.3412", "ask": "...", ...}}
    bid = dados["USDBRL"]["bid"]
    return float(bid)


# ---------------------------------------------------------------------------
# Montagem da mensagem (usada pelos dois métodos de envio)
# ---------------------------------------------------------------------------
def montar_mensagem(cotacao, remetente, destinatario):
    """Cria o e-mail com email.mime (texto simples + HTML)."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    mensagem = MIMEMultipart("alternative")
    mensagem["Subject"] = f"Alerta RPA - Dólar a R$ {cotacao:.4f}"
    mensagem["From"] = remetente
    mensagem["To"] = destinatario

    texto = (
        "Olá!\n\n"
        f"A cotação atual do Dólar (compra) é R$ {cotacao:.4f}.\n"
        f"Consulta feita em {agora} via AwesomeAPI.\n\n"
        "Mensagem automática - Lab 12 RPA (RA 1926102)."
    )
    html = (
        "<h2>Alerta de Cotação</h2>"
        f"<p>Dólar (compra): <b>R$ {cotacao:.4f}</b></p>"
        f"<p>Consulta feita em {agora} via AwesomeAPI.</p>"
        "<small>Mensagem automática - Lab 12 RPA (RA 1926102).</small>"
    )
    mensagem.attach(MIMEText(texto, "plain", "utf-8"))
    mensagem.attach(MIMEText(html, "html", "utf-8"))
    return mensagem


def imprimir_mock(metodo, mensagem):
    """Mostra o e-mail no terminal quando não há credenciais configuradas."""
    print(f"\n----- [MOCK {metodo}] e-mail que seria enviado -----")
    print(f"De: {mensagem['From']}")
    print(f"Para: {mensagem['To']}")
    print(f"Assunto: {mensagem['Subject']}")
    corpo = mensagem.get_payload()[0].get_payload(decode=True).decode("utf-8")
    print(corpo)
    print("-" * 50)


# ---------------------------------------------------------------------------
# 3 - Envio via SMTP
# ---------------------------------------------------------------------------
def enviar_email_smtp(cotacao):
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO") or remetente

    mensagem = montar_mensagem(
        cotacao, remetente or "remetente@exemplo.com", destinatario or "destino@exemplo.com"
    )

    if not (remetente and senha_app):
        imprimir_mock("SMTP", mensagem)
        return "SMTP: credenciais ausentes - e-mail impresso como mock"

    with smtplib.SMTP(SMTP_HOST, SMTP_PORTA, timeout=20) as servidor:
        servidor.starttls()               # liga a criptografia TLS
        servidor.login(remetente, senha_app)
        servidor.send_message(mensagem)
    return f"SMTP: e-mail enviado para {destinatario}"


# ---------------------------------------------------------------------------
# 4 - Envio via Gmail API (OAuth 2.0)
# ---------------------------------------------------------------------------
def obter_servico_gmail():
    """Autentica com OAuth 2.0 e devolve o cliente da Gmail API."""
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
            # Abre o navegador na 1ª execução para você autorizar o app
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w", encoding="utf-8") as arquivo:
            arquivo.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def enviar_email_gmail_api(cotacao):
    remetente = os.getenv("EMAIL_REMETENTE") or "me"
    destinatario = os.getenv("EMAIL_DESTINATARIO") or os.getenv("EMAIL_REMETENTE")
    mensagem = montar_mensagem(cotacao, remetente, destinatario or "destino@exemplo.com")

    if not os.path.exists(CREDENTIALS_FILE) or not destinatario:
        imprimir_mock("GMAIL API", mensagem)
        return "Gmail API: credentials.json ou destinatário ausente - e-mail impresso como mock"

    service = obter_servico_gmail()
    # A Gmail API recebe o e-mail inteiro em base64 URL-safe no campo "raw"
    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode("utf-8")
    enviado = service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return f"Gmail API: e-mail enviado para {destinatario} (id {enviado['id']})"


# ---------------------------------------------------------------------------
# 5 - Execução
# ---------------------------------------------------------------------------
def main():
    try:
        cotacao = buscar_cotacao_dolar()
    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Falha ao consultar a API: {erro}")
        return
    print(f"Cotação do Dólar (bid): R$ {cotacao:.4f}")

    # Cada envio tem seu próprio try/except: a falha de um não impede o outro
    try:
        print(enviar_email_smtp(cotacao))
    except Exception as erro:
        print(f"SMTP: falha no envio - {erro}")

    try:
        print(enviar_email_gmail_api(cotacao))
    except Exception as erro:
        print(f"Gmail API: falha no envio - {erro}")


if __name__ == "__main__":
    main()
