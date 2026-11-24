
import os
import base64
import smtplib
import requests

from pathlib import Path
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Permissão necessária para enviar e-mails pela Gmail API.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Caminho da pasta onde este arquivo está salvo.
PASTA_ATUAL = Path(__file__).resolve().parent


def buscar_cotacao():
    """Consulta a cotação do dólar na AwesomeAPI."""

    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    resposta = requests.get(url, timeout=15)

    # Verifica se a requisição foi realizada com sucesso.
    resposta.raise_for_status()

    # Converte a resposta JSON em um dicionário Python.
    dados = resposta.json()

    # Extrai o valor de compra do dólar.
    cotacao = float(dados["USDBRL"]["bid"])

    print(f"Cotação atual do dólar: R$ {cotacao:.2f}")

    return cotacao


def criar_mensagem(cotacao):
    """Monta o conteúdo do e-mail."""

    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    mensagem = MIMEText(
        f"A cotação atual do dólar é R$ {cotacao:.2f}."
    )

    mensagem["Subject"] = "Alerta de cotação do dólar"
    mensagem["From"] = remetente or "automacao@exemplo.com"
    mensagem["To"] = destinatario or "destinatario@exemplo.com"

    return mensagem


def enviar_email_smtp(cotacao):
    """Envia um e-mail utilizando o protocolo SMTP."""

    remetente = os.getenv("EMAIL_REMETENTE")
    senha = os.getenv("EMAIL_SENHA_APP")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    # Confere se as três variáveis de ambiente estão configuradas.
    if not all([remetente, senha, destinatario]):
        print("\n[SMTP] Credenciais não configuradas.")
        print("[SMTP] Simulação de envio:")
        print(criar_mensagem(cotacao).as_string())
        return

    mensagem = criar_mensagem(cotacao)

    # Conecta ao servidor Gmail e inicia uma conexão segura.
    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()

        # Autentica a conta utilizando a Senha de App.
        servidor.login(remetente, senha)

        # Envia o e-mail.
        servidor.send_message(mensagem)

    print("[SMTP] E-mail enviado com sucesso!")


def enviar_email_gmail_api(cotacao):
    """Envia um e-mail utilizando a Gmail API."""

    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")

    arquivo_credenciais = PASTA_ATUAL / "credentials.json"
    arquivo_token = PASTA_ATUAL / "token.json"

    # Sem credenciais ou destinatário, realiza uma simulação.
    if not arquivo_credenciais.exists() or not destinatario:
        print("\n[Gmail API] Credenciais não configuradas.")
        print("[Gmail API] Simulação de envio:")
        print(criar_mensagem(cotacao).as_string())
        return

    credenciais = None

    # Verifica se já existe um token de autenticação.
    if arquivo_token.exists():
        credenciais = Credentials.from_authorized_user_file(
            str(arquivo_token), SCOPES
        )

    # Atualiza o token expirado ou inicia uma nova autenticação.
    if not credenciais or not credenciais.valid:
        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(
                str(arquivo_credenciais), SCOPES
            )

            credenciais = fluxo.run_local_server(port=0)

        # Salva o token para não precisar autenticar novamente.
        arquivo_token.write_text(credenciais.to_json(), encoding="utf-8")

    # Cria o serviço de acesso à Gmail API.
    servico = build("gmail", "v1", credentials=credenciais)

    mensagem = criar_mensagem(cotacao)

    # Codifica a mensagem no formato base64 URL-safe.
    mensagem_codificada = base64.urlsafe_b64encode(
        mensagem.as_bytes()
    ).decode("utf-8")

    # Envia a mensagem pela Gmail API.
    resultado = servico.users().messages().send(
        userId="me",
        body={"raw": mensagem_codificada}
    ).execute()

    print(
        f"[Gmail API] E-mail enviado com sucesso! "
        f"ID: {resultado.get('id')}"
    )


def main():
    """Executa a consulta e os dois métodos de envio."""

    print("Iniciando o bot de cotação do dólar...\n")

    try:
        cotacao = buscar_cotacao()
    except Exception as erro:
        print(f"Erro ao consultar a cotação: {erro}")
        return

    # Cada método possui seu próprio tratamento de erros.
    try:
        enviar_email_smtp(cotacao)
    except Exception as erro:
        print(f"[SMTP] Erro ao enviar e-mail: {erro}")

    try:
        enviar_email_gmail_api(cotacao)
    except Exception as erro:
        print(f"[Gmail API] Erro ao enviar e-mail: {erro}")

    print("\nExecução do bot finalizada.")


if __name__ == "__main__":
    main()
