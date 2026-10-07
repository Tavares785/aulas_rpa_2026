import sys
import time
import pyautogui

# Configurações de segurança e resiliência do PyAutoGUI
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def executar_robo():
    # 1. Pressiona a tecla Win / Super
    pyautogui.press('win')
    
    # Identifica o sistema operacional para abrir o editor correto
    sistema = sys.platform
    if sistema.startswith('linux'):
        editor = 'gedit'
    else:
        editor = 'notepad'
        
    # 2. Digita o nome do aplicativo e pressiona Enter
    pyautogui.write(editor)
    pyautogui.press('enter')
    
    # 3. Aguarda 2 segundos para o aplicativo carregar
    time.sleep(2)
    
    # 4. Digita o texto de forma visível
    texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"
    pyautogui.write(texto)
    
    # 5. Executa o atalho para salvar (Ctrl + S)
    pyautogui.hotkey('ctrl', 's')
    
    time.sleep(1)

    pyautogui.write("status_bot.txt")
    pyautogui.press('enter')

if __name__ == "__main__":
    executar_robo()
