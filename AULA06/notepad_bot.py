"""
Lab 06 - Controle de perifericos com PyAutoGUI e seguranca fail-safe.

O robo abre o editor de texto do sistema pelo menu iniciar, digita uma
linha de status e salva o arquivo como status_bot.txt.

SEGURANCA: se algo sair do controle, jogue o mouse para um dos cantos da
tela. Com FAILSAFE ligado, o PyAutoGUI levanta FailSafeException e o robo
para na hora.

Instalar: pip install pyautogui
Rodar (no Windows, fora do WSL): python AULA06/notepad_bot.py
"""
import platform
import subprocess
import time

import pyautogui

# Medidas de seguranca exigidas pelo lab.
pyautogui.FAILSAFE = True   # mouse no canto da tela = parada de emergencia
pyautogui.PAUSE = 0.5       # meio segundo de folga depois de cada comando

TEXTO_STATUS = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
NOME_ARQUIVO = "status_bot.txt"
ESPERA_APLICATIVO = 2


def nome_do_editor():
    """Notepad no Windows, gedit no Linux."""
    if platform.system() == "Windows":
        return "notepad"
    return "gedit"


def abrir_editor():
    """Abre o menu iniciar (tecla Win/Super), busca o editor e da Enter."""
    pyautogui.press("win")
    time.sleep(1)  # tempo para o menu iniciar aparecer
    pyautogui.write(nome_do_editor(), interval=0.05)
    pyautogui.press("enter")
    time.sleep(ESPERA_APLICATIVO)


def digitar_status():
    """Digita o texto de forma visivel, letra por letra.

    pyautogui.write so sabe digitar caracteres ASCII e pula os acentos
    ("Relatório", "Execução"). Por isso as letras acentuadas sao coladas
    pela area de transferencia, e o resto e digitado normalmente.
    """
    for letra in TEXTO_STATUS:
        if letra.isascii():
            pyautogui.write(letra)
        else:
            colar(letra)
        time.sleep(0.03)


def colar(texto):
    """Coloca o texto na area de transferencia e cola com Ctrl+V."""
    if platform.system() == "Windows":
        # "utf-16" inclui o BOM, que o clip.exe usa para entender acentos.
        subprocess.run(["clip"], input=texto.encode("utf-16"), check=True)
    else:
        subprocess.run(["xclip", "-selection", "clipboard"],
                       input=texto.encode("utf-8"), check=True)
    pyautogui.hotkey("ctrl", "v")


def salvar_arquivo():
    """Ctrl+S, digita o nome do arquivo e confirma com Enter."""
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1.5)  # espera a janela "Salvar como" abrir
    pyautogui.write(NOME_ARQUIVO, interval=0.05)
    pyautogui.press("enter")


def main():
    print("Robo iniciando em 3 segundos. Mouse no canto da tela = parar.")
    time.sleep(3)
    try:
        abrir_editor()
        digitar_status()
        salvar_arquivo()
    except pyautogui.FailSafeException:
        print("Parada de emergencia acionada (FAILSAFE). Robo interrompido.")
        return
    print(f"Pronto: texto digitado e arquivo salvo como {NOME_ARQUIVO}.")


if __name__ == "__main__":
    main()
