"""""
Para interromper em emergência: mova o mouse para qualquer canto da tela.
"""
 
import sys
import time
 
import pyautogui
import pygetwindow as gw
import pyperclip
 
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
 
APLICATIVO = "notepad"
TEXTO = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
NOME_ARQUIVO = "status_bot.txt"
ESPERA_CARREGAMENTO = 3  # seconds
 
 
def digitar_texto(texto: str) -> None:
    pyperclip.copy(texto)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
 
 
def salvo_com_sucesso(tentativas: int = 5) -> bool:
    nome_base = NOME_ARQUIVO.rsplit(".", 1)[0]  # "status_bot"
    for _ in range(tentativas):
        try:
            janela = gw.getActiveWindow()
            if janela is not None:
                print(f"[debug] título da janela: {janela.title!r}")
                if nome_base in janela.title:
                    return True
        except Exception:
            pass
        time.sleep(0.5)
    return False
 
 
def main() -> None:
    print("Iniciando robô em 2 segundos... (mova o mouse a um canto para abortar)")
    time.sleep(2)
 
    pyautogui.press("win")
    time.sleep(1)
 
    pyautogui.write(APLICATIVO, interval=0.1)
    pyautogui.press("enter")
 
    time.sleep(ESPERA_CARREGAMENTO)
 
    digitar_texto(TEXTO)
 
    pyautogui.hotkey("ctrl", "s")
    time.sleep(1.5)  # waits 4 the wdow "save as" 2 open
    pyautogui.write(NOME_ARQUIVO, interval=0.05)
    pyautogui.press("enter")
    time.sleep(1)
 
    if not salvo_com_sucesso():
        # "Save to Documents instead?" prompt is up
        pyautogui.press("y")      # Yes
        time.sleep(1)             # wait 4 dialog 2 swch 2 Documents
        pyautogui.press("enter")  # click Save again
        time.sleep(1)
 
    if salvo_com_sucesso():
        print(f"Concluído! Arquivo '{NOME_ARQUIVO}' salvo.")
    else:
        print("Algo deu errado: o arquivo pode não ter sido salvo.")
 
 
if __name__ == "__main__":
    try:
        main()
    except pyautogui.FailSafeException:
        print("Execução abortada pelo FAILSAFE (mouse no canto da tela).")
        sys.exit(1)