import csv
import time
import pyautogui

# --- CONFIGURAÇÕES DE SEGURANÇA E TIMING ---
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # Pausa essencial para o navegador processar as mudanças de campo

def preencher_google_forms_oficial():
    print("🤖 Robô do Google Forms Iniciado com Todos os Campos!")
    print("⏳ Você tem 5 segundos para clicar na caixa de texto do 'RA' no navegador...")
    time.sleep(5)
    
    # Aponta para o arquivo oficial de notas da pasta
    caminho_csv = 'AULA07/notas_alunos.csv'
    
    try:
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=';')
            
            for index, linha in enumerate(leitor, start=1):
                nome = linha['Nome']
                ra = linha['RA']
                np1 = linha['Nota01']
                tf1 = linha['TF01']
                np2 = linha['Notao2']  # Puxa o cabeçalho original com o erro de digitação
                tf2 = linha['TF02']
                
                print(f"[{index}] Preenchendo: {nome} (RA: {ra})")
                
                # --- SEQUÊNCIA DE PREENCHIMENTO NO GOOGLE FORMS ---
                pyautogui.write(ra)
                pyautogui.press('tab')
                
                pyautogui.write(nome)
                pyautogui.press('tab')
                
                pyautogui.write(np1)
                pyautogui.press('tab')
                
                pyautogui.write(np2)
                pyautogui.press('tab')
                
                pyautogui.write(tf1)
                pyautogui.press('tab')
                
                pyautogui.write(tf2)
                pyautogui.press('tab')
                
                # --- ENVIO DO FORMULÁRIO ---
                pyautogui.press('enter')
                print("⏳ Aguardando confirmação de envio...")
                time.sleep(3)
                
                # --- RECARREGAR PÁGINA (ESTRATÉGIA ANTI-BUG) ---
                pyautogui.hotkey('ctrl', 'r') 
                time.sleep(3)
                
                # Foca novamente no primeiro campo (RA) após o refresh
                pyautogui.press('tab')
                time.sleep(0.5)
                print(f"✅ Aluno {nome} enviado com sucesso!\n")
                
        print("🎯 Concluído! Todos os alunos do arquivo oficial foram processados.")
        
    except FileNotFoundError:
        print(f"❌ Erro: Não foi possível localizar o arquivo CSV em: {caminho_csv}")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    preencher_google_forms_oficial()
