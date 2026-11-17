import time
import pyautogui

# Configurações de segurança e pausas
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# 1. Pressionar a tecla Win (ou Super) para abrir o menu iniciar
pyautogui.press('win')
time.sleep(1)

# 2. Digitar "notepad" e pressionar Enter
pyautogui.write('notepad', interval=0.1)
pyautogui.press('enter')

# 3. Aguardar 2 segundos para o aplicativo carregar completamente
time.sleep(2)

# 4. Digitar o texto de forma visível com um pequeno intervalo por caractere
texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
pyautogui.write(texto, interval=0.05)

# 5. Executar o atalho para salvar o arquivo (Ctrl + S)
pyautogui.hotkey('ctrl', 's')
time.sleep(1)

# 6. Digitar o nome do arquivo e confirmar com Enter
pyautogui.write('status_bot.txt', interval=0.1)
pyautogui.press('enter')