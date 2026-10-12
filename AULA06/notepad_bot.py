
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

pyautogui.press('win')
pyautogui.write('notepad', interval=0.1)
pyautogui.press('enter')

pyautogui.sleep(2)

pyautogui.write(
    'Relatório de Execução Automática - RPA PyAutoGUI Ativo!',
    interval=0.05
)

pyautogui.hotkey('ctrl', 's')
pyautogui.sleep(1)
pyautogui.write('status_bot.txt', interval=0.1)
pyautogui.press('enter')
