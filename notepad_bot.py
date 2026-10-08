import pyautogui
import time

# Configurações de segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# Abre o menu do sistema
pyautogui.press("win")

# Procura e abre o Bloco de Notas
pyautogui.write("notepad")
pyautogui.press("enter")

# Aguarda o aplicativo carregar
time.sleep(2)

# Digita o texto solicitado
pyautogui.write(
    "Relatório de Execução Automática - RPA PyAutoGUI Ativo!",
    interval=0.03
)

# Salva o arquivo
pyautogui.hotkey("ctrl", "s")

# Aguarda a janela de salvamento
time.sleep(1)

# Digita o nome do arquivo
pyautogui.write("status_bot.txt")
pyautogui.press("enter")
