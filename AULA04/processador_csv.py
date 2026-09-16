import logging

#CONFIGURAÇÃO DO LOG:

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",  
    handlers=[
        logging.FileHandler("execucao_bot.log", encoding="utf-8"),
        logging.StreamHandler()

    ]
)

logging.info("Bot iniciado.")


#FUNÇÃO PROCESSAR ARQUIVO 


def processar_arquivo(caminho: str):
    
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            for linha in arquivo:
                logging.info(f"Linha lida: {linha.strip()}")
        logging.info("Arquivo lido com sucesso!")
    except FileNotFoundError:
        logging.error(f"Arquivo não encontrado: {caminho}")
    except Exception as e:
        logging.error(f"Ocorreu um erro: {e}") 
    finally:
        logging.info("Processo finalizado")

#EXEMPLOS PARA TESTAR BOT
processar_arquivo("dados.csv")
processar_arquivo("arquivo_inexistente.csv")