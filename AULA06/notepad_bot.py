"""
AULA 06 - Controle de Periféricos e Segurança Fail-Safe (PyAutoGUI)

Robô que abre o Bloco de Notas (Windows) ou gedit (Linux), digita um
relatório e salva o arquivo via atalho de teclado.

Requer: pip install pyautogui
"""

import sys
import time

import pyautogui

# ---------------------------------------------------------------------------
# Configurações de segurança obrigatórias
# ---------------------------------------------------------------------------
pyautogui.FAILSAFE = True   # mover o mouse ao canto superior esquerdo aborta
pyautogui.PAUSE = 0.5       # pausa (segundos) entre cada comando

# ---------------------------------------------------------------------------
# Constantes do robô
# ---------------------------------------------------------------------------
TEXTO_RELATORIO: str = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
NOME_ARQUIVO: str = "status_bot.txt"
TEMPO_CARGA_APP: int = 2    # segundos para o aplicativo carregar


def abrir_editor() -> None:
    """Abre o Bloco de Notas (Windows) ou gedit (Linux) via menu iniciar."""
    if sys.platform.startswith("win"):
        # Pressiona a tecla Win para abrir o menu Iniciar
        pyautogui.press("win")
        time.sleep(0.8)
        # Digita o nome do aplicativo na busca
        pyautogui.write("notepad", interval=0.05)
        pyautogui.press("enter")
    else:
        # Linux: pressiona a tecla Super para abrir o launcher
        pyautogui.press("super")
        time.sleep(0.8)
        pyautogui.write("gedit", interval=0.05)
        pyautogui.press("enter")

    # Aguarda o aplicativo carregar completamente
    time.sleep(TEMPO_CARGA_APP)


def digitar_relatorio() -> None:
    """Digita o texto do relatório no editor aberto."""
    # typewrite não suporta caracteres acentuados; usa pyperclip via hotkey
    # ou write com interval para tornar a digitação visível.
    # Para compatibilidade com acentos, usamos pyautogui.write com o texto
    # em ASCII puro, ou hotkey copy-paste. Aqui usamos write char a char.
    pyautogui.write(TEXTO_RELATORIO, interval=0.05)


def salvar_arquivo() -> None:
    """Salva o arquivo via Ctrl+S, insere o nome e confirma com Enter."""
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)  # aguarda a janela de diálogo de salvar abrir
    # Limpa qualquer nome pré-preenchido e digita o nome desejado
    pyautogui.hotkey("ctrl", "a")
    pyautogui.write(NOME_ARQUIVO, interval=0.05)
    pyautogui.press("enter")


def executar_bot() -> None:
    """Ponto de entrada principal do robô."""
    print("Iniciando bot... Você tem 3 segundos para preparar o ambiente.")
    time.sleep(3)

    print("Abrindo editor de texto...")
    abrir_editor()

    print(f"Digitando relatório: {TEXTO_RELATORIO}")
    digitar_relatorio()

    print(f"Salvando arquivo como: {NOME_ARQUIVO}")
    salvar_arquivo()

    print("Bot finalizado com sucesso.")


if __name__ == "__main__":
    executar_bot()
