import pyautogui
import time

# Configurações de segurança
pyautogui.FAILSAFE = True   # mover o mouse para o canto superior esquerdo aborta
pyautogui.PAUSE = 0.5       # pausa de meio segundo entre cada comando


# Abrir o menu iniciar (Windows) ou dash (Linux)
pyautogui.press('win')  # no Linux pode ser 'super'

# Digitar o nome do editor
pyautogui.write('notepad')  # ou 'gedit' no Linux
pyautogui.press('enter')

# Esperar o app carregar
time.sleep(2)

# Digitar o texto
pyautogui.write("Relatório de Execução Automática - RPA PyAutoGUI Ativo!")

# Atalho para salvar
pyautogui.hotkey('ctrl', 's')

# Nome do arquivo
pyautogui.write('status_bot.txt')
pyautogui.press('enter')
