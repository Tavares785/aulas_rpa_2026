"""
AULA 12 - Integracao de Sistemas via APIs REST e Notificacoes E-mail (SMTP e Gmail API)

Aluno: Kaua David Dantas Mendonca
RA: 6326260
"""

import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

URL_AWESOMEAPI = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA_ATUAL = Path(__file__).resolve().parent
ARQUIVO_CREDENCIAIS = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", PASTA_ATUAL / "credentials.json"))
ARQUIVO_TOKEN = Path(os.getenv("GOOGLE_TOKEN_FILE", PASTA_ATUAL / "token.json"))


def consultar_cotacao_dolar() -> dict[str, Any]:
    """Consulta a API publica AwesomeAPI e retorna os dados da cotacao USD-BRL."""
    print(f"Consultando cotação em: {URL_AWESOMEAPI}")
    resposta = requests.get(URL_AWESOMEAPI, timeout=15)
    resposta.raise_for_status()
    dados = resposta.json()

    cotacao_usd = dados.get("USDBRL", {})
    valor_compra_bid = cotacao_usd.get("bid", "0.00")
    print(f"Cotação obtida com sucesso! Valor de compra (bid): R$ {valor_compra_bid}")
    return cotacao_usd


def montar_mensagem_email(cotacao: str, remetente: str, destinatario: str) -> MIMEMultipart:
    """Monta a estrutura MIME do e-mail com a cotacao formatada."""
    msg = MIMEMultipart()
    msg["Subject"] = f"Alerta de Cotacao: Dolar Comercial R$ {cotacao}"
    msg["From"] = remetente
    msg["To"] = destinatario

    corpo = (
        "Prezado(a),\n\n"
        "Este é um alerta automatizado de câmbio.\n\n"
        f"A cotação atual do Dólar Comercial (bid) é: R$ {cotacao}\n\n"
        "Atenciosamente,\n"
        "Bot RPA Integrador"
    )
    msg.attach(MIMEText(corpo, "plain", "utf-8"))
    return msg


def enviar_email_smtp(cotacao: str) -> bool:
    """Envia notificacao por e-mail utilizando o protocolo SMTP com STARTTLS."""
    print("\n--- [1/2] Envio de E-mail via Protocolo SMTP ---")
    remetente = os.getenv("EMAIL_REMETENTE")
    senha_app = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO", remetente or "destinatario@exemplo.com")

    if not remetente or not senha_app:
        print("[MOCK SMTP] Credenciais de ambiente (EMAIL_REMETENTE / EMAIL_SENHA_APP) não configuradas.")
        print("Exibindo estrutura da mensagem no terminal para simulação:")
        msg_mock = montar_mensagem_email(cotacao, remetente or "bot@empresa.com", destinatario)
        print(f"  De     : {msg_mock['From']}")
        print(f"  Para   : {msg_mock['To']}")
        print(f"  Assunto: {msg_mock['Subject']}")
        print("  Status : Simulação concluída com sucesso (sem envio real).")
        return True

    msg = montar_mensagem_email(cotacao, remetente, destinatario)
    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as servidor:
            servidor.starttls()
            servidor.login(remetente, senha_app)
            servidor.send_message(msg)
        print(f"E-mail enviado via SMTP com sucesso para {destinatario}!")
        return True
    except Exception as erro:
        print(f"Falha ao disparar e-mail via SMTP: {erro}")
        return False


def obter_cliente_gmail_api():
    """Autentica via OAuth 2.0 e inicializa o cliente da Gmail API."""
    creds = None
    if ARQUIVO_TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(ARQUIVO_TOKEN), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not ARQUIVO_CREDENCIAIS.exists():
                raise FileNotFoundError(
                    f"Arquivo de credenciais OAuth 2.0 não encontrado: {ARQUIVO_CREDENCIAIS}"
                )
            fluxo = InstalledAppFlow.from_client_secrets_file(str(ARQUIVO_CREDENCIAIS), SCOPES)
            creds = fluxo.run_local_server(port=0)

        with open(ARQUIVO_TOKEN, "w", encoding="utf-8") as token_file:
            token_file.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def enviar_email_gmail_api(cotacao: str) -> bool:
    """Envia notificacao por e-mail utilizando a API REST oficial do Gmail."""
    print("\n--- [2/2] Envio de E-mail via Gmail API (Google API) ---")
    destinatario = os.getenv("EMAIL_DESTINATARIO", "destinatario@exemplo.com")
    msg = montar_mensagem_email(cotacao, "me", destinatario)

    if not ARQUIVO_CREDENCIAIS.exists() and not ARQUIVO_TOKEN.exists():
        print("[MOCK GMAIL API] Arquivo credentials.json não configurado.")
        print("Exibindo estrutura da mensagem no terminal para simulação:")
        raw_bytes = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        print(f"  Para    : {msg['To']}")
        print(f"  Assunto : {msg['Subject']}")
        print(f"  Raw b64 : {raw_bytes[:40]}... (tamanho: {len(raw_bytes)} bytes)")
        print("  Status  : Simulação concluída com sucesso (sem envio real).")
        return True

    try:
        service = obter_cliente_gmail_api()
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        resposta = service.users().messages().send(userId="me", body={"raw": raw}).execute()
        id_mensagem = resposta.get("id", "N/D")
        print(f"E-mail enviado via Gmail API com sucesso! ID da mensagem: {id_mensagem}")
        return True
    except Exception as erro:
        print(f"Falha ao enviar e-mail via Gmail API: {erro}")
        return False


def main() -> None:
    """Fluxo principal de integracao de API REST e envio de alertas."""
    print("=" * 60)
    print("INICIANDO BOT DE COTACAO E ALERTA DE CAMBIO")
    print("=" * 60)

    try:
        dados_cotacao = consultar_cotacao_dolar()
        cotacao_bid = dados_cotacao.get("bid", "0.00")
    except Exception as erro:
        print(f"Erro ao consultar API de câmbio: {erro}")
        return

    # 1. Envio por SMTP com isolamento de erro
    try:
        enviar_email_smtp(cotacao_bid)
    except Exception as erro_smtp:
        print(f"Exceção capturada no envio SMTP: {erro_smtp}")

    # 2. Envio por Gmail API com isolamento de erro
    try:
        enviar_email_gmail_api(cotacao_bid)
    except Exception as erro_gmail:
        print(f"Exceção capturada no envio Gmail API: {erro_gmail}")

    print("\n" + "=" * 60)
    print("PROCESSO DO LAB 12 CONCLUIDO")
    print("=" * 60)


if __name__ == "__main__":
    main()
