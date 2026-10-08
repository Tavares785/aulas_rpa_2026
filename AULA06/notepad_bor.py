import pyautogui as pu
pu.FAILSAFE = True
pu.PAUSE = 0.7
pu.hotkey('WIN')
pu.write('notepad')
pu.hotkey('enter')
pu.PAUSE 
pu.write('Relatorio de Execucao Automatica - RPA PyAutoGUI Ativo!', )
pu.PAUSE
pu.hotkey('ctrl', 's')
pu.write('status_bot.txt')
pu.hotkey('enter')