import time
import pandas as pd
import pyautogui

pyautogui.PAUSE = 1.0
pyautogui.FAILSAFE = True

Notas_exemplos = "./Notas_exemplos.csv"

def lancar_Notas_csv(Notas_exemplos):
    print("\nLendo o arquivo CSV...")
    try:
        df = pd.read_csv(Notas_exemplos,sep=';')
    except FileNotFoundError:
        print(f"Erro: Arquivo '{Notas_exemplos}' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    print("\nATENÇÃO: Posicione o foco do mouse no primeiro campo do Formulário Google.")
    print("O script começará em 5 segundos...")
    time.sleep(5)

    for index, row in df.iterrows():
        ra = str(row['RA'])
        nome = str(row['Nome'])
        Nota = str(row['Nota01'])

        pyautogui.write(ra)
        pyautogui.press('tab')
        
        pyautogui.write(nome)
        pyautogui.press('tab')
        
        pyautogui.write(Nota)
        pyautogui.press('tab')



        print(f"[{index + 1}/{len(df)}] Registro do RA {ra} preenchido.")
        time.sleep(1)

    print("\nLançamento concluído com sucesso!")


def consultar_por_ra(Notas_exemplos):
    try:
        df = pd.read_csv(Notas_exemplos,sep=';')
        df['RA'] = df['RA'].astype(str).str.strip()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{Notas_exemplos}' não encontrado.")
        return
    except KeyError:
        print("Erro: A coluna 'RA' não foi encontrada no arquivo CSV.")
        return
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        return

    while True:
        ra_busca = input("\nDigite o RA para consulta (ou digite 'sair' para voltar ao menu): ").strip()
        
        if ra_busca.lower() == 'sair':
            break

        resultado = df[df['RA'] == ra_busca]

        if not resultado.empty:
            print("\n--- Informações Encontradas ---")

            for coluna in resultado.columns:
                valor = resultado.iloc[0][coluna]
                print(f"{coluna}: {valor}")
            print("-" * 30)
        else:
            print(f"Nenhum registro encontrado para o RA: {ra_busca}")

def main():
    caminho_padrao_csv = "./Notas_exemplos.csv"

    while True:
        print("\n=== SISTEMA DE GESTÃO DE NotaS (CSV) ===")
        print("1. Lançar Notas no Formulário Google (via PyAutoGUI)")
        print("2. Consultar Notas por RA (no CSV)")
        print("3. Sair")
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == '1':
            caminho = input(f"Digite o caminho do CSV [Pressione ENTER para '{caminho_padrao_csv}']: ").strip()
            if not caminho:
                caminho = caminho_padrao_csv
            lancar_Notas_csv(caminho)

        elif opcao == '2':
            caminho = input(f"Digite o caminho do CSV [Pressione ENTER para '{caminho_padrao_csv}']: ").strip()
            if not caminho:
                caminho = caminho_padrao_csv
            consultar_por_ra(caminho)

        elif opcao == '3':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()