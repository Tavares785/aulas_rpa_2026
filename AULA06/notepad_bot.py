
import time                # Módulo: controle de tempo.
import pyautogui as pg     # Módulo: automação de teclado e mouse.
import pyperclip           # Módulo: área de transferência.
from pathlib import Path  # Classe: manipulação de caminhos de arquivos.


# ============================================================
# 1. CONFIGURAÇÕES DE SEGURANÇA
# ============================================================

pg.FAILSAFE = True  # Atributo: permite interromper pelo canto da tela.
pg.PAUSE = 0.5       # Atributo: pausa de 0,5 s entre comandos PyAutoGUI.


# ============================================================
# 2. DEFINIÇÃO DO TEXTO E ARQUIVO
# ============================================================

# Variável: texto exigido pelo professor.
texto = "Relatório de Execução Automática - RPA PyAutoGUI Ativo!"

# Path(__file__): caminho do script atual.
# .resolve(): método que obtém o caminho absoluto.
# .parent: propriedade que retorna a pasta do script.
# /: operador que combina caminhos.
# Exemplo: D:\Projeto\status_bot.txt.
arquivo = Path(__file__).resolve().parent / "status_bot.txt"


# ============================================================
# 3. ABERTURA DO BLOCO DE NOTAS
# ============================================================

pg.press("win")  # Função: pressiona a tecla Windows.

# .write(): função que simula digitação.
# interval: argumento que define o intervalo entre caracteres.
pg.write("notepad", interval=0.1)  # Digita "notepad".

pg.press("enter")  # Função: confirma a pesquisa.

time.sleep(2)  # Função: aguarda 2 segundos para abrir.

pg.hotkey("ctrl", "n")  # Função: cria um documento vazio.


# ============================================================
# 4. DIGITAÇÃO VISÍVEL DO RELATÓRIO
# ============================================================

# for: percorre cada caractere da string.
for caractere in texto:

    # .isascii(): método que verifica caracteres ASCII.
    # Exemplo: "R" → True | "ó" → False.
    if caractere.isascii():

        # Digita o caractere com intervalo de 0,1 segundo.
        pg.write(caractere, interval=0.1)

    else:

        # .copy(): função que copia o caractere acentuado.
        # Exemplo: "ó" → área de transferência.
        pyperclip.copy(caractere)

        # .hotkey(): função que executa Ctrl + V.
        pg.hotkey("ctrl", "v")


# ============================================================
# 5. SALVAMENTO DO ARQUIVO
# ============================================================

pg.hotkey("ctrl", "s")  # Função: abre a janela Salvar Como.

time.sleep(1)  # Aguarda a janela aparecer.

# str(): função que converte o caminho Path para string.
# .copy(): copia o caminho completo do arquivo.
pyperclip.copy(str(arquivo))

pg.hotkey("ctrl", "v")  # Cola o caminho no campo Nome do arquivo.

pg.press("enter")  # Confirma o salvamento.

time.sleep(1)  # Aguarda o sistema salvar.


# ============================================================
# 6. VERIFICAÇÃO DO ARQUIVO
# ============================================================

# .is_file(): método que verifica se o arquivo existe.
if arquivo.is_file():
    print(f"Arquivo encontrado: {arquivo}")
else:
    print("Arquivo não encontrado. Verifique a janela de salvamento.")
