import time
import pyautogui

print("Coloque o mouse em cima do campo NOME em 5 segundos...")
time.sleep(5)
print("Posição encontrada:", pyautogui.position())