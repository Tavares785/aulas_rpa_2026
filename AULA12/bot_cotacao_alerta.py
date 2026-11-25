import requests
import smtplib
from email.mime.text import MIMEText
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


URL_API = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def busca_dolar(link_api):
    try:
        resposta = requests.get(link_api, timeout=10)
        resposta.raise_for_status() # retorna um exceção caso o servidor retorne um código de erro

        print(f'Sucesso! status: {resposta.status_code}')
        dados = resposta.json()
        dolar = float(dados['USDBRL']['bid'])
        return dolar
    
    except requests.exceptions.RequestException as erro: # mãe de todas as exceções, captura todas as diferentes falhas
        print(f'Erro ao acessar a API: {erro}')
        return None
    
    except KeyError as e:
        print(f'Chave inexistente na API: {e}')
        return None
    
    except ValueError as e:
        print(f'Valor não convertido: {e}')
        return None

def enviar_email_smtp(cotacao):
    remetente = os.getenv('EMAIL_REMETENTE')
    senha_app = os.getenv('EMAIL_SENHA_APP')
    destinatario = os.getenv('EMAIL_DESTINATARIO')

    if not remetente or not senha_app or not destinatario:
        return f'Cotação atual do Dólar: R${cotacao:.2f}' # MOCK

    corpo = f'Cotação atual do Dólar R${cotacao:.2f}'

    msg = MIMEText(corpo, 'plain', 'utf-8')
    msg['Subject'] = 'Valor do Dolar em Reais'
    msg['From'] = remetente
    msg['To'] = destinatario

    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=10) as servidor:
            servidor.starttls() #criptografa a conexão
            servidor.login(remetente, senha_app) # autenticação
            servidor.sendmail(remetente, destinatario, msg.as_string())
            return 'Email enviado'
    except Exception as erro:
        return f'EMAIL RECUSADO: {erro}'

def enviar_email_gmail_api(
        cotacao,
        caminho_token='AULA12/token.json',
        caminho_credencial='AULA12/credentials.json',
):
    destinatario = os.getenv('EMAIL_DESTINATARIO')

    #MOCK
    if(
        not os.path.exists(caminho_token)
        and not os.path.exists(caminho_credencial)
    ) or not destinatario:
        return f'Cotação atual do Dólar R${cotacao:.2f}'

    creds = None

    if os.path.exists(caminho_token):
        creds = Credentials.from_authorized_user_file(caminho_token, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                caminho_credencial, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(caminho_token, 'w') as token:
            token.write(creds.to_json())

    corpo = f'Alerta de Cotação: o Dólar (USD-BRL) está cotado a R$ {cotacao:.2f}.'

    msg = MIMEText(corpo, 'plain', 'utf-8')
    msg['To'] = destinatario
    msg['Subject'] = 'Alerta de Cotação do Dólar (Gmail API)'

    # Converte a mensagem para bytes, codifica em Base64 URL-safe e volta para str
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')

    service = build('gmail', 'v1', credentials=creds)
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
    print("E-mail enviado com sucesso via Gmail API!")

def main():
    cotacao = busca_dolar(URL_API)

    # 1. Guarda de entrada: interrompe o fluxo se a coleta falhar
    if cotacao is None:
        print("Não foi possível obter a cotação do dólar. Envios cancelados.")
        return

    print(f"Cotação atual: R$ {cotacao:.2f}\n")

    # 2. Canal SMTP isolado
    try:
        resultado_smtp = enviar_email_smtp(cotacao)
        if resultado_smtp:
            print(f"[SMTP] {resultado_smtp}")
    except Exception as erro:
        print(f"[SMTP] Erro ao processar envio: {erro}")

    # 3. Canal Gmail API isolado
    try:
        resultado_api = enviar_email_gmail_api(cotacao)
        if resultado_api:
            print(f"[Gmail API] {resultado_api}")
    except Exception as erro:
        print(f"[Gmail API] Erro ao processar envio: {erro}")


if __name__ == "__main__":
    main()

