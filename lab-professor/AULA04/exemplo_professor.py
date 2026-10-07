"""
AULA 04 - Persistencia, Excecoes e Auditoria
Exemplo do PROFESSOR

Tema didatico: with (context manager), try/except/finally e logging.
Cenario de negocio: conciliacao de leituras de sensores IoT. Um coletor de
campo grava medicoes de temperatura por sensor em um arquivo de texto; o bot
le essas medicoes, audita cada leitura e fecha a trilha mesmo em caso de erro.
O proprio script gera o arquivo de medicoes em tempo de execucao para rodar
em qualquer maquina, sem depender de dados externos.
"""
import logging

# Configuracao de logging: grava em arquivo E mostra no console --------------
# Dois handlers em paralelo: um para a trilha persistente, outro para o console.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler("auditoria_sensores.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

# Nome do arquivo de medicoes gerado em runtime no dominio de sensores IoT.
ARQUIVO_MEDICOES = "leituras_sensores.txt"


def gerar_medicoes_demo() -> None:
    """Cria um .txt de medicoes de temperatura so para a demo rodar sozinha."""
    # Formato simples por linha: identificador do sensor e temperatura em Celsius.
    with open(ARQUIVO_MEDICOES, "w", encoding="utf-8") as arquivo:
        arquivo.write("sensor;temperatura_c\n")
        arquivo.write("SENSOR-A1;21.4\n")
        arquivo.write("SENSOR-B2;23.9\n")
        arquivo.write("SENSOR-C3;19.7\n")


def conciliar_leituras(caminho: str) -> int:
    """Le as medicoes do sensor com tratamento de erro e trilha de auditoria.

    Retorna a quantidade de leituras conciliadas (0 quando o arquivo falta).
    """
    total_conciliado = 0
    try:
        # 'with' garante o fechamento do arquivo mesmo diante de excecao.
        with open(caminho, "r", encoding="utf-8") as arquivo:
            for numero, linha in enumerate(arquivo, start=1):
                conteudo = linha.strip()
                # Primeira linha e cabecalho; serve de referencia na auditoria.
                if numero == 1:
                    logging.info("Cabecalho identificado: %s", conteudo)
                    continue
                logging.info("Leitura %d conciliada: %s", numero - 1, conteudo)
                total_conciliado += 1
    except FileNotFoundError:
        # Caminho de erro: registra em nivel ERROR sem derrubar o processo.
        logging.error("Arquivo de medicoes nao encontrado: %s", caminho)
    finally:
        # Bloco sempre executado: fecha a trilha de auditoria da tentativa.
        logging.info("Fim da conciliacao de '%s'.", caminho)
    return total_conciliado


if __name__ == "__main__":
    gerar_medicoes_demo()
    quantidade = conciliar_leituras(ARQUIVO_MEDICOES)
    logging.info("Total de leituras conciliadas: %d", quantidade)

    # DICA DE AULA: rode de novo apontando para um arquivo inexistente
    # para mostrar o log de ERROR + o finally sempre executando:
    conciliar_leituras("coletor_offline.txt")

    # Limpeza opcional dos artefatos da demo:
    # import os
    # os.remove(ARQUIVO_MEDICOES)
