"""
AULA 13 - Filas, Assincrono e Resiliencia
Exemplo do PROFESSOR

Tema didatico: padrao Produtor-Consumidor com queue.Queue aplicado a uma
fila de chamados de suporte (helpdesk). Cada chamado e reprocessado com
Retry e backoff exponencial quando o atendimento falha.

Observacao de dependencia: o retry e implementado manualmente (sem lib
externa). Caso a biblioteca 'tenacity' esteja instalada, demonstramos como
ela poderia ser usada; se ela nao existir, seguimos com o retry manual.
"""
import queue
import random
import time

# Guard de ImportError: usamos 'tenacity' apenas se estiver disponivel.
# O exemplo continua funcionando mesmo sem a biblioteca instalada.
try:
    import tenacity  # noqa: F401

    TENACITY_DISPONIVEL = True
except ImportError:
    TENACITY_DISPONIVEL = False
    print(
        "[INFO] Biblioteca 'tenacity' nao encontrada. "
        "Usando retry manual. "
        "Para instalar: pip install tenacity"
    )


def produtor(fila: "queue.Queue[dict]", quantidade: int) -> None:
    """Gera chamados de suporte e coloca cada um na fila do helpdesk."""
    for i in range(1, quantidade + 1):
        chamado = {"id": i, "ticket": f"TCK-{2000 + i}"}
        fila.put(chamado)
        print(f"[PRODUTOR] Abriu chamado {chamado['ticket']}")


def atender_com_retry(chamado: dict, max_tentativas: int = 3) -> bool:
    """Tenta atender o chamado; em falha, espera 2^n segundos (backoff)."""
    for tentativa in range(1, max_tentativas + 1):
        # Simula instabilidade do sistema de suporte: 60% de sucesso.
        sucesso = random.random() > 0.4
        if sucesso:
            print(
                f"[OK] {chamado['ticket']} atendido "
                f"(tentativa {tentativa})"
            )
            return True
        espera = 2 ** tentativa  # backoff exponencial: 2s, 4s, 8s...
        print(
            f"[RETRY] {chamado['ticket']} falhou. "
            f"Aguardando {espera}s antes de nova tentativa..."
        )
        # Sleep encurtado para a aula; na pratica use 'espera'.
        time.sleep(0.05)
    print(f"[FALHA] {chamado['ticket']} esgotou as tentativas.")
    return False


def consumidor(fila: "queue.Queue[dict]") -> None:
    """Worker que retira chamados da fila e os atende ate esvaziar."""
    while not fila.empty():
        chamado = fila.get()
        atender_com_retry(chamado)
        fila.task_done()


def main() -> None:
    """Monta a fila, enfileira chamados e dispara o atendimento."""
    random.seed(7)  # resultado reproduzivel para a aula
    fila_chamados: "queue.Queue[dict]" = queue.Queue()
    produtor(fila_chamados, quantidade=100)
    print("-" * 40)
    consumidor(fila_chamados)


if __name__ == "__main__":
    main()
    # DICA DE AULA: explique por que o backoff exponencial evita "martelar"
    # um sistema de suporte que ja esta sobrecarregado, dando tempo para ele
    # se recuperar entre as tentativas.
