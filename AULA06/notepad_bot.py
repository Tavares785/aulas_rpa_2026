import platform
import time
import pyautogui

# Configurações de segurança e latência operacional
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

# Detectar sistema operacional para definir o comando correto
is_windows = platform.system() == "Windows"
app_command = "notepad" if is_windows else "gedit"

# 1. Pressionar a tecla Win / Super
pyautogui.press("win")

# 2. Digitar o nome do aplicativo e pressionar Enter
pyautogui.write(app_command, interval=0.1)
pyautogui.press("enter")

# 3. Aguardar 2 segundos para o aplicativo carregar
time.sleep(2)

# 4. Digitar o texto solicitado de forma visível
texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
pyautogui.write(texto, interval=0.05)

# 5. Salvar o arquivo (Ctrl + S), digitar o nome e confirmar com Enter
pyautogui.hotkey("ctrl", "s")
time.sleep(1)  # Breve pausa para garantir a abertura da caixa de diálogo
pyautogui.write("status_bot.txt", interval=0.1)
pyautogui.press("enter")
