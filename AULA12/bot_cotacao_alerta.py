"""
Lab 12 - Integração de Sistemas via APIs REST e Notificações por E-mail.

Aluna: Emanuela Oliveira da Costa
RA: 6326085

Fluxo do bot:
1. Consome a API pública da AwesomeAPI (GET) para obter a cotação do Dólar.
2. Extrai o valor de compra (campo "bid") do JSON retornado.
3. Envia um e-mail de alerta via SMTP (smtplib + email.mime).
4. Envia o mesmo e-mail via Gmail API (OAuth 2.0 + users.messages.send).

Credenciais SMTP são lidas das variáveis de ambiente:
    EMAIL_REMETENTE, EMAIL_SENHA_APP, EMAIL_DESTINATARIO

Para a Gmail API é necessário o arquivo credentials.json (OAuth 2.0 -
Aplicativo para computador). O token gerado fica em token.json.
Nenhum desses arquivos deve ser commitado (já estão no .gitignore).

Se as credenciais não estiverem configuradas (ou se MOCK_EMAIL=true),
o e-mail é apenas impresso no terminal (modo mock).
"""

import base64
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    GOOGLE_DISPONIVEL = True
except ImportError:
    GOOGLE_DISPONIVEL = False

URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SMTP_SERVIDOR = "smtp.gmail.com"
SMTP_PORTA = 587
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CREDENCIAIS = os.path.join(PASTA_SCRIPT, "credentials.json")
ARQUIVO_TOKEN = os.path.join(PASTA_SCRIPT, "token.json")


def modo_mock():
    """Retorna True quando o envio real de e-mails deve ser simulado."""
    return os.getenv("MOCK_EMAIL", "false").strip().lower() == "true"


def buscar_cotacao_dolar():
    """Consulta a AwesomeAPI e retorna o valor de compra (bid) do Dólar."""
    resposta = requests.get(URL_API, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    cotacao = float(dados["USDBRL"]["bid"])
    return cotacao


def montar_mensagem(cotacao, remetente, destinatario):
    """Monta a mensagem de e-mail (MIME) com a cotação informada."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = f"Alerta RPA - Cotação do Dólar: R$ {cotacao:.4f}"

    corpo = (
        "Olá!\n\n"
        "Segue a cotação atual do Dólar (USD-BRL) obtida pelo bot de RPA:\n\n"
        f"    Valor de compra (bid): R$ {cotacao:.4f}\n"
        f"    Consulta realizada em: {agora}\n\n"
        "Fonte: AwesomeAPI (economia.awesomeapi.com.br)\n\n"
        "Mensagem automática enviada pelo bot_cotacao_alerta.py."
    )
    mensagem.attach(MIMEText(corpo, "plain", "utf-8"))
    return mensagem


def imprimir_mock(metodo, mensagem):
    """Exibe o e-mail no terminal no lugar do envio real."""
    print(f"\n----- [MOCK {metodo}] E-mail que seria enviado -----")
    print(f"De: {mensagem['From']}")
    print(f"Para: {mensagem['To']}")
    print(f"Assunto: {mensagem['Subject']}")
    for parte in mensagem.walk():
        if parte.get_content_type() == "text/plain":
            print(parte.get_payload(decode=True).decode("utf-8"))
    print("-" * 55)


def enviar_email_smtp(cotacao):
    """Envia o alerta de cotação via SMTP (Gmail + Senha de App)."""
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    mensagem = montar_mensagem(
        cotacao,
        remetente or "remetente@exemplo.com",
        destinatario or "destinatario@exemplo.com",
    )

    if modo_mock() or not (remetente and senha_app and destinatario):
        imprimir_mock("SMTP", mensagem)
        return "SMTP: credenciais não configuradas - e-mail exibido em modo mock."

    with smtplib.SMTP(SMTP_SERVIDOR, SMTP_PORTA, timeout=30) as servidor:
        servidor.starttls()
        servidor.login(remetente, senha_app)
        servidor.send_message(mensagem)

    return f"SMTP: e-mail enviado com sucesso para {destinatario}."


def obter_credenciais_google():
    """Autentica via OAuth 2.0 e retorna as credenciais da Gmail API."""
    credenciais = None
    if os.path.exists(ARQUIVO_TOKEN):
        credenciais = Credentials.from_authorized_user_file(ARQUIVO_TOKEN, SCOPES)

    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(ARQUIVO_CREDENCIAIS, SCOPES)
            credenciais = flow.run_local_server(port=0)
        with open(ARQUIVO_TOKEN, "w", encoding="utf-8") as arquivo:
            arquivo.write(credenciais.to_json())

    return credenciais


def enviar_email_gmail_api(cotacao):
    """Envia o alerta de cotação via Gmail API (users.messages.send)."""
    remetente = os.getenv("EMAIL_REMETENTE", "me")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    mensagem = montar_mensagem(
        cotacao,
        remetente,
        destinatario or "destinatario@exemplo.com",
    )

    pode_enviar = (
        GOOGLE_DISPONIVEL
        and destinatario
        and (os.path.exists(ARQUIVO_CREDENCIAIS) or os.path.exists(ARQUIVO_TOKEN))
    )
    if modo_mock() or not pode_enviar:
        imprimir_mock("GMAIL API", mensagem)
        return "Gmail API: credenciais não configuradas - e-mail exibido em modo mock."

    credenciais = obter_credenciais_google()
    service = build("gmail", "v1", credentials=credenciais)

    raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode("utf-8")
    enviado = service.users().messages().send(userId="me", body={"raw": raw}).execute()

    return f"Gmail API: e-mail enviado com sucesso (id: {enviado.get('id')})."


def main():
    print("=== Bot de Cotação do Dólar com Alerta por E-mail ===")

    try:
        cotacao = buscar_cotacao_dolar()
    except (requests.RequestException, KeyError, ValueError) as erro:
        print(f"Erro ao consultar a cotação na AwesomeAPI: {erro}")
        return

    print(f"Cotação atual do Dólar (bid): R$ {cotacao:.4f}")

    try:
        print(enviar_email_smtp(cotacao))
    except Exception as erro:
        print(f"SMTP: falha no envio do e-mail - {erro}")

    try:
        print(enviar_email_gmail_api(cotacao))
    except Exception as erro:
        print(f"Gmail API: falha no envio do e-mail - {erro}")

    print("=== Execução finalizada ===")


if __name__ == "__main__":
    main()
