import os
import csv
import logging

logger = logging.getLogger("BotResiliente")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("execucao_bot.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def processar_arquivo(caminho: str):
    logger.info(f"Iniciando tentativa de processamento do arquivo: {caminho}")
    
    try:
        with open(caminho, mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.reader(arquivo)
            for index, linha in enumerate(leitor_csv, start=1):
                if not linha:
                    continue
                logger.info(f"Linha {index} processada com sucesso: {linha}")
                
    except FileNotFoundError as e:
        logger.error(f"Erro crítico: O arquivo especificado não foi encontrado no caminho '{caminho}'. Detalhes: {e}")
        
    except Exception as e:
        logger.error(f"Ocorreu um erro inesperado durante a leitura: {e}")
        
    finally:
        logger.info(f"Fim da tentativa de processamento para o arquivo: {caminho}")


if __name__ == "__main__":
    processar_arquivo("dados_inexistentes.csv")
    
    arquivo_teste = "clientes_teste.csv"
    with open(arquivo_teste, mode='w', encoding='utf-8', newline='') as f:
        escritor = csv.writer(f)
        escritor.writerow(["ID", "Nome", "Status"])
        escritor.writerow(["001", "Ana Silva", "Ativo"])
        escritor.writerow(["002", "Bruno Costa", "Pendente"])

    processar_arquivo(arquivo_teste)
    
    if os.path.exists(arquivo_teste):
        os.remove(arquivo_teste)
