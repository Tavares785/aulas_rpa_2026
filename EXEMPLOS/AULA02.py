emails_pendentes = [
    {"cliente": "ACME", "tentativas": 0, "status": "PENDENTE"},
    {"cliente": "Globex", "tentativas": 5, "status": "PENDENTE"},   # estourou limite
    {"cliente": "Umbrella", "tentativas": 1, "status": "ENVIADO"},  # ja enviado -> pular
    {"cliente": "Stark", "tentativas": 0, "status": "BLOQUEADO"},   # para tudo!
    {"cliente": "Wayne", "tentativas": 2, "status": "PENDENTE"},
]

LIMITE_TENTATIVAS = 3


def processar_fila(fila: list) -> None:
    for item in fila:
        cliente = item["cliente"]

        # continue: pula para o proximo sem processar
        if item["status"] == "ENVIADO":
            print(f"[SKIP] {cliente}: e-mail ja enviado.")
            continue

        # break: condicao critica interrompe TODO o processamento
        if item["status"] == "BLOQUEADO":
            print(f"[CRITICO] {cliente} bloqueado. Interrompendo a fila!")
            break

        # if/elif/else: regra de negocio principal
        if item["tentativas"] >= LIMITE_TENTATIVAS:
            print(f"[ALERTA] {cliente}: limite de tentativas atingido.")
        else:
            print(f"[OK] Enviando cobranca para {cliente}...")


if __name__ == "__main__":
    processar_fila(emails_pendentes)