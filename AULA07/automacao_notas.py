import time
import pyautogui
from processar_dados import limpar_nome, limpar_ra, converter_nota

pyautogui.PAUSE = 0.05
pyautogui.FAILSAFE = True

def carregar_dados():
    alunos = []
    with open("notas_alunos.csv", mode="r", encoding="utf-8") as f:
        linhas = f.readlines()

    for linha in linhas[1:]:
        if not linha.strip():
            continue
        partes = linha.strip().split(";")
        
        nome = limpar_nome(partes[0])
        ra = limpar_ra(partes[1])
        n1 = converter_nota(partes[2], teto_maximo=10.0)
        tf1 = converter_nota(partes[3], teto_maximo=2.0)
        n2 = converter_nota(partes[4], teto_maximo=10.0)
        tf2 = converter_nota(partes[5], teto_maximo=2.0)

        s1 = (n1 * 0.8) + tf1
        s2 = (n2 * 0.8) + tf2
        media_final = round((s1 + s2) / 2.0, 2)
        situacao = "Aprovado" if media_final >= 6.0 else "Reprovado"

        alunos.append({
            "ra": ra,
            "nome": nome,
            "media": f"{media_final:.2f}",
            "situacao": situacao
        })
    return alunos

def executar_robo():
    alunos = carregar_dados()
    
    print("=" * 60)
    print("ROBÔ DE LANÇAMENTO DE NOTAS PRONTO")
    print(f"Total de registos a lançar: {len(alunos)}")
    print("Tem 5 SEGUNDOS para clicar no campo 'Matrícula / RA' do Portal...")
    print("=" * 60)

    for i in range(5, 0, -1):
        print(f"A iniciar em {i}...")
        time.sleep(1)

    print("\nA lançar notas...")
    aprovados = 0
    reprovados = 0

    for idx, aluno in enumerate(alunos, start=1):
        ra_texto = "" if aluno["ra"] == "SEM_RA" else aluno["ra"]
        pyautogui.write(ra_texto)
        pyautogui.press("tab")

        pyautogui.write(aluno["nome"])
        pyautogui.press("tab")

        pyautogui.write(aluno["media"])
        pyautogui.press("tab")

        pyautogui.write(aluno["situacao"])
        pyautogui.press("tab")

        pyautogui.press("enter")

        if aluno["situacao"] == "Aprovado":
            aprovados += 1
        else:
            reprovados += 1

        print(f"[{idx}/100] Lançado: {aluno['nome']} - Média: {aluno['media']} ({aluno['situacao']})")
        time.sleep(0.04)

    print("\n" + "=" * 60)
    print("ESTATÍSTICAS FINAIS DE FECHO")
    print("=" * 60)
    print(f"Total de Alunos Processados: {len(alunos)}")
    print(f"Aprovados: {aprovados} ({(aprovados/len(alunos))*100:.1f}%)")
    print(f"Reprovados: {reprovados} ({(reprovados/len(alunos))*100:.1f}%)")

if __name__ == "__main__":
    executar_robo()
    