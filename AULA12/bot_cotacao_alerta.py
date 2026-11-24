import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

URL_API = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
ESCOPOS = ["https://www.googleapis.com/auth/gmail.send"]

# Os arquivos do Google ficam na mesma pasta deste script
pasta_script = os.path.dirname(os.path.abspath(__file__))
ARQ_CREDENCIAIS = os.path.join(pasta_script, "credentials.json")
ARQ_TOKEN = os.path.join(pasta_script, "token.json")


def buscar_cotacao():
    # Pede o JSON pra API e pega o valor de compra (bid) do dolar
    resposta = requests.get(URL_API, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()
    return float(dados["USDBRL"]["bid"])


def montar_corpo(cotacao):
    return "A cotacao atual do Dolar (compra) e R$ " + f"{cotacao:.2f}"


def montar_mensagem(cotacao, remetente, destinatario):
    # Monta o e-mail com a biblioteca email.mime
    mensagem = MIMEMultipart()
    if remetente:
        mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = "Alerta: cotacao do Dolar (USD-BRL)"
    mensagem.attach(MIMEText(montar_corpo(cotacao), "plain", "utf-8"))
    return mensagem


def enviar_email_smtp(cotacao):
    # Credenciais vem das variaveis de ambiente (nunca no codigo)
    remetente = os.environ.get("EMAIL_REMETENTE")
    senha = os.environ.get("EMAIL_SENHA_APP")
    destinatario = os.environ.get("EMAIL_DESTINATARIO")

    # Sem credenciais: mostra o e-mail no terminal (mock)
    if not remetente or not senha or not destinatario:
        print("[SMTP] Credenciais nao configuradas. E-mail (mock):")
        print("  Para:", destinatario or "(nao definido)")
        print("  Texto:", montar_corpo(cotacao))
        return

    try:
        mensagem = montar_mensagem(cotacao, remetente, destinatario)
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remetente, senha)
        servidor.send_message(mensagem)
        servidor.quit()
        print("[SMTP] E-mail enviado com sucesso!")
    except Exception as erro:
        print("[SMTP] Falha no envio:", erro)


def enviar_email_gmail_api(cotacao):
    remetente = os.environ.get("EMAIL_REMETENTE")
    destinatario = os.environ.get("EMAIL_DESTINATARIO")
    tem_google = os.path.exists(ARQ_CREDENCIAIS) or os.path.exists(ARQ_TOKEN)

    # Sem credenciais do Google: mostra o e-mail no terminal (mock)
    if not tem_google or not destinatario:
        print("[Gmail API] Credenciais nao configuradas. E-mail (mock):")
        print("  Para:", destinatario or "(nao definido)")
        print("  Texto:", montar_corpo(cotacao))
        return

    try:
        # 1. Carrega o token salvo, se ja existir
        credenciais = None
        if os.path.exists(ARQ_TOKEN):
            credenciais = Credentials.from_authorized_user_file(
                ARQ_TOKEN, ESCOPOS
            )

        # 2. Se nao tem token valido, faz o login (OAuth 2.0)
        if credenciais is None or not credenciais.valid:
            if (
                credenciais is not None
                and credenciais.expired
                and credenciais.refresh_token
            ):
                credenciais.refresh(Request())
            else:
                fluxo = InstalledAppFlow.from_client_secrets_file(
                    ARQ_CREDENCIAIS, ESCOPOS
                )
                credenciais = fluxo.run_local_server(port=0)
            with open(ARQ_TOKEN, "w") as arquivo:
                arquivo.write(credenciais.to_json())

        # 3. Monta o e-mail e codifica em base64 URL-safe
        mensagem = montar_mensagem(cotacao, remetente, destinatario)
        raw = base64.urlsafe_b64encode(mensagem.as_bytes()).decode()

        # 4. Envia pela Gmail API
        service = build("gmail", "v1", credentials=credenciais)
        service.users().messages().send(
            userId="me", body={"raw": raw}
        ).execute()
        print("[Gmail API] E-mail enviado com sucesso!")
    except Exception as erro:
        print("[Gmail API] Falha no envio:", erro)


def main():
    try:
        cotacao = buscar_cotacao()
    except Exception as erro:
        print("Falha ao buscar a cotacao:", erro)
        return

    print("Cotacao do Dolar (compra): R$", f"{cotacao:.2f}")

    # Cada envio e independente: se um falhar, o outro ainda roda
    enviar_email_smtp(cotacao)
    enviar_email_gmail_api(cotacao)


if __name__ == "__main__":
    main()
