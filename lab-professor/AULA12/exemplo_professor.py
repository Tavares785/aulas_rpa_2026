"""
AULA 12 - APIs REST e Notificacoes por E-mail
Exemplo do PROFESSOR (envio REAL via Gmail API)

Cenario de negocio: ALERTA DE AGENDA. O bot consulta os feriados nacionais
do ano na BrasilAPI (sem chave), monta um e-mail com os proximos feriados e
ENVIA pela Gmail API (https://gmail.googleapis.com) usando OAuth2.


Requer:
    pip install requests google-api-python-client google-auth-httplib2 \
        google-auth-oauthlib
"""
from __future__ import annotations

import base64
import os
import sys
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import requests

API_FERIADOS = "https://brasilapi.com.br/api/feriados/v1/{ano}"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

PASTA = Path(__file__).resolve().parent
CREDENCIAIS = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", PASTA / "credentials.json"))
TOKEN = Path(os.getenv("GOOGLE_TOKEN_FILE", PASTA / "token.json"))


def consultar_feriados(ano: int) -> list[dict[str, str]]:
    """GET na API publica; devolve a lista de feriados (JSON -> list[dict])."""
    resposta = requests.get(API_FERIADOS.format(ano=ano), timeout=15)
    resposta.raise_for_status()
    return resposta.json()


def selecionar_proximos(
    feriados: list[dict[str, str]], limite: int = 3, a_partir_de: date | None = None
) -> list[dict[str, str]]:
    """Ordena por data e devolve os proximos 'limite' feriados a partir de hoje."""
    hoje = (a_partir_de or date.today()).isoformat()
    futuros = [f for f in feriados if f.get("date", "") >= hoje]
    return sorted(futuros, key=lambda item: item["date"])[:limite]


def montar_email(proximos: list[dict[str, str]], destinatarios: list[str]) -> MIMEMultipart:
    """Monta a mensagem com email.mime. O 'From' e preenchido pelo Gmail."""
    linhas = ["Alerta de agenda - proximos feriados nacionais:", ""]
    for feriado in proximos:
        linhas.append(f"- {feriado.get('date', '?')}: {feriado.get('name', '?')}")
    corpo = "\n".join(linhas)

    msg = MIMEMultipart()
    msg["Subject"] = "Lembrete de agenda: feriados a caminho"
    msg["To"] = ", ".join(destinatarios)
    msg.attach(MIMEText(corpo, _subtype="plain", _charset="utf-8"))
    return msg


def obter_servico_gmail():
    """Autentica via OAuth2 (reusa/renova token.json) e devolve o cliente Gmail."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENCIAIS.exists():
                raise FileNotFoundError(
                    f"Arquivo de credenciais OAuth nao encontrado: {CREDENCIAIS}"
                )
            fluxo = InstalledAppFlow.from_client_secrets_file(str(CREDENCIAIS), SCOPES)
            creds = fluxo.run_local_server(port=0)
        TOKEN.write_text(creds.to_json(), encoding="utf-8")
        TOKEN.chmod(0o600)
    return build("gmail", "v1", credentials=creds)


def enviar_email(servico, msg: MIMEMultipart) -> str:
    """Envia via users.messages.send (POST gmail.googleapis.com). Retorna o id."""
    bruto = base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")
    resposta = servico.users().messages().send(userId="me", body={"raw": bruto}).execute()
    return resposta["id"]


def exibir_email(msg: MIMEMultipart) -> None:
    print("  Assunto:", msg["Subject"])
    print("  Para   :", msg["To"])
    print("  Corpo  :")
    for parte in msg.get_payload():
        print(parte.get_payload(decode=True).decode("utf-8", errors="replace"))


def main() -> int:
    dry_run = "--dry-run" in sys.argv[1:]

    try:
        feriados = consultar_feriados(date.today().year)
    except requests.RequestException as erro:
        print(f"Nao foi possivel consultar a API de feriados: {erro}")
        return 1

    proximos = selecionar_proximos(feriados)
    print(f"Feriados retornados pela API: {len(feriados)}")
    if not proximos:
        print("Nenhum feriado restante neste ano. Nada a enviar.")
        return 0

    destino_env = os.getenv("EMAIL_DESTINO", "")
    destinatarios = [d.strip() for d in destino_env.split(",") if d.strip()]

    if dry_run:
        email = montar_email(proximos, destinatarios or ["(sua conta Gmail)"])
        print("[DRY-RUN] E-mail montado, nao enviado:")
        exibir_email(email)
        return 0

    try:
        servico = obter_servico_gmail()
        if not destinatarios:
            perfil = servico.users().getProfile(userId="me").execute()
            destinatarios = [perfil["emailAddress"]]
        email = montar_email(proximos, destinatarios)
        mensagem_id = enviar_email(servico, email)
    except ImportError:
        print(
            "Instale as dependencias: pip install google-api-python-client "
            "google-auth-httplib2 google-auth-oauthlib"
        )
        return 1
    except Exception as erro:  # noqa: BLE001 - HttpError, erros de OAuth, rede
        print(f"Falha ao enviar e-mail pela Gmail API: {erro}")
        return 1

    print(f"E-mail enviado para {email['To']} (id Gmail: {mensagem_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
