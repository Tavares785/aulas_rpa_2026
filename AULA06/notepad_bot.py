import pyautogui
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

print("Vai começar em 3 segundos, tira a mão do mouse!")
time.sleep(3)

pyautogui.press('win')
time.sleep(1)
pyautogui.write('notepad')
pyautogui.press('enter')
time.sleep(1)
pyautogui.write('Relatorio de Execucao Automatica - RPA PyAutoGUI Ativo!')

pyautogui.hotkey('ctrl', 's')
time.sleep(1)
pyautogui.write('status_bot.txt')
pyautogui.press('enter')

print("concluido!")