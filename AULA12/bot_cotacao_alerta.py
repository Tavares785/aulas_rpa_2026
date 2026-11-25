
import os
import requests
import smtplib
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ==========================================
# CONFIGURAÇÕES
# ==========================================

URL_API = (
    "https://economia.awesomeapi.com.br/json/last/USD-BRL"
)

ESCOPO_GMAIL = [
    "https://www.googleapis.com/auth/gmail.send"
]


# ==========================================
# 1. CONSULTAR COTAÇÃO DO DÓLAR
# ==========================================

def buscar_cotacao():
    """Consulta a cotação do dólar na AwesomeAPI."""

    resposta = requests.get(URL_API, timeout=15)

    resposta.raise_for_status()

    dados = resposta.json()

    cotacao = float(dados["USDBRL"]["bid"])

    print(f"Cotação atual do dólar: R$ {cotacao:.4f}")

    return cotacao


# ==========================================
# 2. MONTAR MENSAGEM DE E-MAIL
# ==========================================

def criar_email(cotacao, remetente, destinatario):
    """Cria uma mensagem de e-mail formatada."""

    mensagem = MIMEMultipart()

    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = "Alerta automático - Cotação do Dólar"

    corpo = f"""
Olá!

Este é um alerta automático de cotação.

Cotação atual do dólar:
R$ {cotacao:.4f}

Valor de compra consultado na AwesomeAPI.

Mensagem enviada automaticamente pelo Python.
"""

    mensagem.attach(MIMEText(corpo, "plain", "utf-8"))

    return mensagem


# ==========================================
# 3. ENVIO DE E-MAIL VIA SMTP
# ==========================================

def enviar_email_smtp(cotacao):
    """Envia um e-mail utilizando o protocolo SMTP."""

    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    # Verifica se as credenciais estão configuradas.
    if not all([remetente, senha, destinatario]):
        print("\n[MOCK SMTP] Credenciais não configuradas.")

        print(
            f"E-mail simulado: Cotação do dólar R$ {cotacao:.4f}"
        )

        return "SIMULADO"

    mensagem = criar_email(
        cotacao,
        remetente,
        destinatario
    )

    # Conexão com o servidor Gmail.
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:

        servidor.starttls()

        servidor.login(remetente, senha)

        servidor.sendmail(
            remetente,
            destinatario,
            mensagem.as_string()
        )

    print("\nE-mail enviado com sucesso via SMTP!")

    return "ENVIADO"


# ==========================================
# 4. ENVIO DE E-MAIL VIA GMAIL API
# ==========================================

def enviar_email_gmail_api(cotacao):
    """Envia um e-mail utilizando a Gmail API."""

    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    if not remetente or not destinatario:
        print("\n[MOCK GMAIL API] Credenciais não configuradas.")

        print(
            f"E-mail simulado: Cotação do dólar R$ {cotacao:.4f}"
        )

        return "SIMULADO"

    if not os.path.exists("credentials.json"):
        print(
            "\n[MOCK GMAIL API] Arquivo credentials.json não encontrado."
        )

        print(
            f"E-mail simulado: Cotação do dólar R$ {cotacao:.4f}"
        )

        return "SIMULADO"

    credenciais = None

    # Verifica se já existe um token salvo.
    if os.path.exists("token.json"):

        credenciais = Credentials.from_authorized_user_file(
            "token.json",
            ESCOPO_GMAIL
        )

    # Renova o token ou realiza a autenticação.
    if credenciais and credenciais.expired and credenciais.refresh_token:

        credenciais.refresh(Request())

    elif not credenciais or not credenciais.valid:

        fluxo = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            ESCOPO_GMAIL
        )

        credenciais = fluxo.run_local_server(port=0)

    # Salva o token para as próximas execuções.
    with open("token.json", "w", encoding="utf-8") as arquivo:
        arquivo.write(credenciais.to_json())

    # Cria o serviço da Gmail API.
    servico = build(
        "gmail",
        "v1",
        credentials=credenciais
    )

    # Monta a mensagem.
    mensagem = criar_email(
        cotacao,
        remetente,
        destinatario
    )

    # Codifica a mensagem em Base64 URL-safe.
    mensagem_codificada = base64.urlsafe_b64encode(
        mensagem.as_bytes()
    ).decode("utf-8")

    corpo = {
        "raw": mensagem_codificada
    }

    # Envia a mensagem pela Gmail API.
    resultado = servico.users().messages().send(
        userId="me",
        body=corpo
    ).execute()

    print("\nE-mail enviado com sucesso via Gmail API!")

    print(f"ID da mensagem: {resultado['id']}")

    return "ENVIADO"


# ==========================================
# 5. PROGRAMA PRINCIPAL
# ==========================================

def main():

    print("=" * 50)
    print("       BOT DE COTAÇÃO DO DÓLAR")
    print("=" * 50)

    # Consulta a cotação.
    try:
        cotacao = buscar_cotacao()

    except requests.RequestException as erro:

        print(f"\nErro ao consultar a API: {erro}")

        return

    except (KeyError, TypeError, ValueError) as erro:

        print(f"\nErro ao processar o JSON: {erro}")

        return

    # Tentativa de envio via SMTP.
    try:

        resultado_smtp = enviar_email_smtp(cotacao)

        print(f"Resultado SMTP: {resultado_smtp}")

    except Exception as erro:

        print(f"\nFalha no envio SMTP: {erro}")

    # Tentativa de envio via Gmail API.
    try:

        resultado_api = enviar_email_gmail_api(cotacao)

        print(f"Resultado Gmail API: {resultado_api}")

    except Exception as erro:

        print(f"\nFalha no envio Gmail API: {erro}")

    print("\nProcessamento finalizado!")


# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":
    main()
