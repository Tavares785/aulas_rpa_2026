
import os
import requests
import smtplib
import base64

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# CONFIGURACOES
URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA = os.path.dirname(os.path.abspath(__file__))

ARQUIVO_CREDENTIALS = os.path.join(PASTA, "credentials.json")
ARQUIVO_TOKEN = os.path.join(PASTA, "token.json")


# 1. CONSULTAR COTACAO DO DOLAR
def buscar_cotacao():
    resposta = requests.get(URL_API, timeout=15)
    resposta.raise_for_status()

    dados = resposta.json()

    cotacao = float(dados["USDBRL"]["bid"])

    print(f"\nCotacao atual do dolar: R$ {cotacao:.4f}")

    return cotacao


# 2. CRIAR MENSAGEM DE EMAIL
def criar_email(cotacao, remetente, destinatario):

    assunto = "Alerta de Cotacao do Dolar"

    corpo = f"""
Ola!

Esta e uma notificacao automatica da cotacao do dolar.

Cotacao atual: R$ {cotacao:.4f}

Mensagem enviada pelo Bot de Cotacao.

Atenciosamente,
Bot de Cotacao
"""

    mensagem = MIMEText(corpo, "plain", "utf-8")

    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    return mensagem


# 3. ENVIAR EMAIL VIA SMTP
def enviar_email_smtp(cotacao):

    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not all([remetente, senha, destinatario]):

        print("\n[MOCK SMTP]")
        print("Credenciais SMTP nao configuradas.")

        mensagem = criar_email(
            cotacao,
            remetente or "Remetente nao configurado",
            destinatario or "Destinatario nao configurado"
        )

        print(mensagem.as_string())

        return False

    mensagem = criar_email(cotacao, remetente, destinatario)

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:

        servidor.ehlo()
        servidor.starttls()
        servidor.ehlo()

        servidor.login(remetente, senha)

        servidor.send_message(mensagem)

    print("\n[SMTP] Email enviado com sucesso!")

    return True


# 4. AUTENTICACAO OAUTH 2.0 DO GOOGLE
def autenticar_gmail():

    credenciais = None

    if os.path.exists(ARQUIVO_TOKEN):

        credenciais = Credentials.from_authorized_user_file(
            ARQUIVO_TOKEN,
            SCOPES
        )

    if credenciais and not credenciais.has_scopes(SCOPES):
        credenciais = None

    if credenciais and credenciais.expired and credenciais.refresh_token:

        credenciais.refresh(Request())

    if not credenciais or not credenciais.valid:

        if not os.path.exists(ARQUIVO_CREDENTIALS):
            raise FileNotFoundError(
                "Arquivo credentials.json nao encontrado."
            )

        fluxo = InstalledAppFlow.from_client_secrets_file(
            ARQUIVO_CREDENTIALS,
            SCOPES
        )

        credenciais = fluxo.run_local_server(port=0)

    with open(ARQUIVO_TOKEN, "w") as arquivo:

        arquivo.write(credenciais.to_json())

    service = build(
        "gmail",
        "v1",
        credentials=credenciais
    )

    return service


# 5. ENVIAR EMAIL VIA GMAIL API
def enviar_email_gmail_api(cotacao):

    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not remetente or not destinatario or not os.path.exists(ARQUIVO_CREDENTIALS):

        print("\n[MOCK GMAIL API]")
        print("Credenciais ou configuracao do Gmail API nao encontradas.")

        mensagem = criar_email(
            cotacao,
            remetente or "Remetente nao configurado",
            destinatario or "Destinatario nao configurado"
        )

        print(mensagem.as_string())

        return False

    mensagem = criar_email(cotacao, remetente, destinatario)

    service = autenticar_gmail()

    # Codificacao Base64 URL-safe
    raw = base64.urlsafe_b64encode(
        mensagem.as_bytes()
    ).decode("utf-8")

    # Envio pela API do Gmail
    resultado = service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

    print("\n[GMAIL API] Email enviado com sucesso!")
    print("ID da mensagem:", resultado["id"])

    return True


# 6. FUNCAO PRINCIPAL
def main():

    print("=" * 45)
    print(" BOT DE COTACAO DO DOLAR")
    print("=" * 45)

    # Consulta da cotacao
    try:

        cotacao = buscar_cotacao()

    except Exception as erro:

        print("\nErro ao consultar a API:")
        print(erro)

        return

    # Envio SMTP
    try:

        resultado_smtp = enviar_email_smtp(cotacao)

        print("Resultado SMTP:", resultado_smtp)

    except Exception as erro:

        print("\nErro no envio SMTP:")
        print(erro)

    # Envio Gmail API
    try:

        resultado_api = enviar_email_gmail_api(cotacao)

        print("Resultado Gmail API:", resultado_api)

    except Exception as erro:

        print("\nErro no envio Gmail API:")
        print(erro)

    print("\nProcesso finalizado!")


# EXECUCAO
if __name__ == "__main__":
    main()
