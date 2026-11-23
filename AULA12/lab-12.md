# Lab 12: Integração de Sistemas via APIs REST (Requests) e Notificações E-mail (SMTP e Gmail API)

## 🎯 Objetivos de Aprendizagem
- Entender a diferença entre automação por UI e comunicação nativa por protocolo de rede.
- Consumir Web APIs REST utilizando verbos HTTP (`GET`) e manipular JSON em dicionários Python.
- Construir e disparar e-mails automáticos via protocolo SMTP usando as bibliotecas `smtplib` e `email.mime`.
- Enviar e-mails pela Gmail API do Google, com autenticação OAuth 2.0, e comparar com o envio via SMTP.

## 💼 Desafio de Mercado
Acionar navegadores por interface gráfica para buscar informações simples (ex: cotação de moedas, validação de CEP ou envio de alertas) gera lentidão e fragilidade. A forma profissional e escalável de automação conecta-se diretamente às APIs dos serviços e envia notificações por e-mail.

---

## 📝 Enunciado (Aluno)

Crie um script integrador `bot_cotacao_alerta.py` que execute os passos:
1. **Consumo de API:** Acesse a API pública da AwesomeAPI para buscar a cotação atual do Dólar (`https://economia.awesomeapi.com.br/json/last/USD-BRL`).
2. **Processamento JSON:** Extraia o valor de compra (`bid`) do Dólar do JSON retornado.
3. **Notificação por E-mail via SMTP:**
   - Construa uma função `enviar_email_smtp(cotacao)` que receba a cotação extraída e monte uma mensagem de e-mail formatada com a biblioteca `email.mime`.
   - Configure o envio usando `smtplib.SMTP` (ex: `smtp.gmail.com`, porta `587`, com `starttls()`).
   - Use uma **Senha de App** do Google (não a senha da conta) e leia credenciais de variáveis de ambiente (`EMAIL_REMETENTE`, `EMAIL_SENHA_APP`, `EMAIL_DESTINATARIO`). Nunca deixe credenciais no código.
4. **Notificação por E-mail via Gmail API (Google API):**
   - Construa uma função `enviar_email_gmail_api(cotacao)` que envie o mesmo e-mail pela **Gmail API** (`users.messages.send`).
   - Instale as dependências: `pip install google-api-python-client google-auth-oauthlib google-auth-httplib2`.
   - No [Google Cloud Console](https://console.cloud.google.com/), crie um projeto, ative a **Gmail API** e crie credenciais **OAuth 2.0 (Aplicativo para computador)**. Baixe o arquivo como `credentials.json`.
   - Use o escopo `https://www.googleapis.com/auth/gmail.send` e autentique com `InstalledAppFlow`. O token gerado fica em `token.json`.
   - Monte a mensagem com `email.mime`, codifique em base64 URL-safe (`base64.urlsafe_b64encode`) e envie no campo `raw`:
     ```python
     service.users().messages().send(userId="me", body={"raw": raw}).execute()
     ```
   - **Não commite** `credentials.json` nem `token.json` (adicione ao `.gitignore`).
5. **Execução:** No `main`, chame as duas funções de envio. Trate exceções de cada uma separadamente (`try/except`), de modo que a falha de um método não impeça a tentativa do outro, e imprima no terminal o resultado de cada envio.
   *(Nota: se as credenciais não estiverem configuradas, imprima o e-mail no terminal como mock em vez de falhar. O CI não executa o script, apenas valida a estrutura do código.)*

---



## 🚀 Entrega

1. No **seu fork**, crie uma branch a partir da `main` com o nome `lab12/SEU_RA` (ex: `lab12/123456`):
   ```bash
   git checkout main
   git pull origin main
   git checkout -b lab12/SEU_RA
   ```
2. Adicione e commite seus arquivos:
   ```bash
   git add .
   git commit -m "lab12: entrega RA SEU_RA"
   ```
3. Suba a branch para o **seu fork**:
   ```bash
   git push origin lab12/SEU_RA
   ```
4. No GitHub, abra um **Pull Request** do seu fork para o repositório do professor (`main`) com o título:
   ```
   [Lab12] Entrega - RA SEU_RA
   ```
5. Aguarde a validação do CI (GitHub Actions) e a revisão do professor.

---
