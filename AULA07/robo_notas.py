import csv
import time
import pyautogui

# Configuração de segurança do PyAutoGUI
# Caso o robô perca o controle, jogue o mouse para o canto superior esquerdo da tela para parar
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5  # Pausa de meio segundo entre comandos para dar estabilidade

def ler_dados_csv(caminho_arquivo):
    """Lê o arquivo CSV e armazena os alunos em uma lista de dicionários."""
    alunos = []
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=';')
            for linha in leitor:
                # Função auxiliar interna com tratamento para "FALTOU"
                def tratar_nota(valor_texto):
                    texto_limpo = valor_texto.strip().upper().replace(',', '.')
                    # Se o aluno faltou ou o campo estiver vazio, a nota vira 0.0
                    if texto_limpo == "FALTOU" or not texto_limpo:
                        return 0.0
                    return float(texto_limpo)

                alunos.append({
                    "Nome": linha["Nome"].strip(),
                    "RA": linha["RA"].strip(),
                    "Nota01": tratar_nota(linha["Nota01"]),
                    "TF01": tratar_nota(linha["TF01"]),
                    "Nota02": tratar_nota(linha["Nota02"]),
                    "TF02": tratar_nota(linha["TF02"])
                })
    except FileNotFoundError:
        print(f"[ERRO] O arquivo {caminho_arquivo} não foi encontrado.")
    except Exception as e:
        print(f"[ERRO] Falha ao ler o arquivo: {e}")
    
    return alunos

def calcular_media_e_status(aluno):
    """Calcula a média final ponderada e define a situação do aluno."""
    # Média do primeiro bimestre (Peso 8 para Nota, Peso 2 para Trabalho Final)
    media_b1 = (aluno["Nota01"] * 8 + aluno["TF01"] * 2) / 10
    # Média do segundo bimestre
    media_b2 = (aluno["Nota02"] * 8 + aluno["TF02"] * 2) / 10
    
    # Média final aritmética simples entre os dois bimestres
    media_final = (media_b1 + media_b2) / 2
    status = "APROVADO" if media_final >= 6.0 else "REPROVADO"
    
    return round(media_final, 2), status

def simular_automacao_desktop(aluno, media_final, status):
    """Simula a interação com o sistema acadêmico legado usando PyAutoGUI."""
    print(f"[PROCESSANDO] Lançando dados do aluno: {aluno['Nome']} (RA: {aluno['RA']})")
    
    # --- EXEMPLO DE FLUXO DE NAVEGAÇÃO VIA TECLADO ---
    # 1. Pesquisa pelo RA
    pyautogui.write(aluno["RA"])
    pyautogui.press("enter")
    time.sleep(1.5)  # Tempo de espera para o sistema carregar o aluno
    
    # 2. Navega até o campo da Nota Final (exemplo usando TAB)
    pyautogui.press("tab")
    pyautogui.write(str(media_final))
    
    # 3. Navega até o campo de Situação/Status
    pyautogui.press("tab")
    pyautogui.write(status)
    
    # 4. Salva o registro
    pyautogui.press("enter")
    time.sleep(1.0)  # Aguarda a confirmação de salvamento do portal antigo

def executar_rpa(caminho_csv):
    """Função principal que coordena a leitura, processamento e estatísticas."""
    alunos = ler_dados_csv(caminho_csv)
    if not alunos:
        return

    # Contadores para estatísticas
    total_alunos = len(alunos)
    aprovados = 0
    reprovados = 0
    soma_medias = 0.0

    print("\n--- INICIANDO AUTOMAÇÃO EM 5 SEGUNDOS ---")
    print("Abra o sistema na tela correta e clique no campo de busca inicial!")
    time.sleep(5)  # Tempo para o usuário mudar de janela e focar no portal

    for aluno in alunos:
        media, status = calcular_media_e_status(aluno)
        
        # Acumula dados para as estatísticas
        soma_medias += media
        if status == "APROVADO":
            aprovados += 1
        else:
            reprovados += 1
            
        # Executa as ações na interface de forma controlada
        simular_automacao_desktop(aluno, media, status)

    # --- EXIBIÇÃO DE ESTATÍSTICAS ---
    media_geral_turma = round(soma_medias / total_alunos, 2) if total_alunos > 0 else 0
    percentual_aprovados = round((aprovados / total_alunos) * 100, 2) if total_alunos > 0 else 0

    print("\n" + "="*40)
    print("        RELATÓRIO DE EXECUÇÃO RPA        ")
    print("="*40)
    print(f"Total de Alunos Processados : {total_alunos}")
    print(f"Quantidade de Aprovados     : {aprovados} ({percentual_aprovados}%)")
    print(f"Quantidade de Reprovados    : {reprovados}")
    print(f"Média Geral da Turma        : {media_geral_turma}")
    print("="*40)

if __name__ == "__main__":
    # Defina o nome do arquivo que você vai usar para testes locais
    executar_rpa("notas_alunos.csv")
