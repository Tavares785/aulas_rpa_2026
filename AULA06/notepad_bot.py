import logging as log
import time
import pyautogui as pa

# Configuração do log
log.basicConfig(
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def config_ambiente():
    pa.FAILSAFE = True
    pa.PAUSE = 0.5
    log.info('Ambiente RPA configurado com sucesso!')


def abrir_editor(comando='mousepad'):
    """Abre o editor de texto especificado no comando com uma validação simples."""
    # se o comando for texto valido, a condição é True e com o Not ela vira False, então o bloco de código não será executado
    if not comando:
        raise ValueError('Comando inválido! Informe o nome do editor de texto.')
    log.info(f'Abrindo o editor de texto: {comando}')
    pa.hotkey('alt', 'f2')  # Atalho para abrir o menu de execução do Xfce4
    pa.write(comando)  # Escreve o comando no editor
    pa.press('enter')  # Pressiona a tecla Enter para executar o comando


def escrever_texto(texto):
    """Escreve o texto especificado no editor de texto aberto."""
    if not texto:
        raise ValueError('Texto inválido! Informe o texto a ser escrito.')
    time.sleep(2)  # Aguarda o editor abrir
    log.info(f'Escrevendo o texto: {texto}')
    pa.write(texto)


def salvar_arquivo(nome_arquivo):
    """Salva o arquivo com o nome especificado."""
    log.info(f'Salvando o arquivo como: {nome_arquivo}')
    pa.hotkey('ctrl', 's')  # Atalho para salvar o arquivo
    time.sleep(1)  # Aguarda a janela de salvar abrir
    pa.write(nome_arquivo)  # Escreve o nome do arquivo
    pa.press('enter')   # Pressiona a tecla Enter para salvar o arquivo


def main():
    try:
        config_ambiente()
        abrir_editor('mousepad')
        mensagem = 'Relatorio de Execucao Automatica - RPA PyAutoGUI Ativo!'
        escrever_texto(mensagem)
        salvar_arquivo('status_bot.txt')
        log.info('Processo concluído com sucesso!')
    except pa.FailSafeException:
        log.warning('Execução interrompida pelo usuário (FailSafe).')
    except ValueError as ve:
        log.error(f'Erro de valor: {ve}')
    except Exception as e:
        log.critical(f'Erro inesperado: {e}')
    finally:
        log.info('Finalizando o robô. Até a próxima!')


if __name__ == '__main__':
    main()
