"""
Lab 06 - Controle de Periféricos e Segurança Fail-Safe
Robô que abre o editor de texto via atalho de teclado,
digita um relatório e salva o arquivo automaticamente.
"""

import pyautogui
import time
import sys

# ─── Configurações de Segurança ──────────────────────────────────────────────
# FAILSAFE: mova o mouse para o canto superior esquerdo para abortar o script
pyautogui.FAILSAFE = True
# PAUSE: intervalo (em segundos) entre cada ação do pyautogui
pyautogui.PAUSE = 0.5

# ─── Detecta o sistema operacional ───────────────────────────────────────────
import platform
SO = platform.system()  # 'Windows', 'Linux' ou 'Darwin'

print(f"[INFO] Sistema detectado: {SO}")
print("[INFO] Iniciando robô em 3 segundos... (mova o mouse para o canto superior esquerdo para cancelar)")
time.sleep(3)

# ─── Passo 1: Abrir o editor de texto via tecla Super/Win ────────────────────
if SO == "Windows":
    print("[PASSO 1] Abrindo menu Iniciar...")
    pyautogui.press("win")
    time.sleep(1)

    print("[PASSO 2] Digitando 'notepad'...")
    pyautogui.typewrite("notepad", interval=0.1)
    pyautogui.press("enter")

else:
    # Linux: usa xdg-open ou o atalho Super para abrir o gedit/notepad
    print("[PASSO 1] Pressionando tecla Super para abrir o launcher...")
    pyautogui.press("super")
    time.sleep(1)

    print("[PASSO 2] Digitando 'gedit'...")
    pyautogui.typewrite("gedit", interval=0.1)
    pyautogui.press("enter")

# ─── Passo 3: Aguardar o aplicativo carregar ─────────────────────────────────
print("[PASSO 3] Aguardando o editor carregar (2s)...")
time.sleep(2)

# ─── Passo 4: Digitar o texto do relatório ───────────────────────────────────
texto = "Relatorio de Execucao Automatica - RPA PyAutoGUI Ativo!"
print(f"[PASSO 4] Digitando: {texto!r}")
pyautogui.typewrite(texto, interval=0.05)

# ─── Passo 5: Salvar o arquivo com Ctrl+S ────────────────────────────────────
print("[PASSO 5] Salvando o arquivo (Ctrl+S)...")
pyautogui.hotkey("ctrl", "s")
time.sleep(1)

# ─── Passo 6: Digitar o nome do arquivo e confirmar ──────────────────────────
nome_arquivo = "status_bot.txt"
print(f"[PASSO 6] Digitando o nome do arquivo: {nome_arquivo!r}")
pyautogui.typewrite(nome_arquivo, interval=0.1)
pyautogui.press("enter")

print("[OK] Robô concluído com sucesso!")

