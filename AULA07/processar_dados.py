import csv
import re

def limpar_nome(nome_bruto: str) -> str:
    """Remove espaços duplos e coloca em formato Nome Sobrenome."""
    if not nome_bruto:
        return "NOME DESCONHECIDO"
    return " ".join(nome_bruto.strip().split()).title()

def limpar_ra(ra_bruto: str) -> str:
    """Extrai somente os números do RA; retorna SEM_RA se não houver."""
    if not ra_bruto:
        return "SEM_RA"
    digitos = re.sub(r"\D", "", ra_bruto)
    return digitos if digitos else "SEM_RA"

def converter_nota(valor_bruto: str, teto_maximo: float) -> float:
    """Trata vírgula, faltas, textos e vazios, convertendo para número float."""
    if not valor_bruto:
        return 0.0
    
    val = valor_bruto.strip().replace(",", ".")
    textos_ausencia = {"faltou", "falta", "n/a", "-", ""}
    if val.lower() in textos_ausencia:
        return 0.0
    
    try:
        nota = float(val)
        if nota < 0.0:
            return 0.0
        return min(nota, teto_maximo)
    except ValueError:
        return 0.0

def processar():
    alunos_limpos = []

    with open("notas_alunos.csv", mode="r", encoding="utf-8") as f:
        linhas = f.readlines()

    # Pula o cabeçalho
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

        # Regra de notas: P1 (80%) + TF1 e P2 (80%) + TF2
        semestre_1 = (n1 * 0.8) + tf1
        semestre_2 = (n2 * 0.8) + tf2
        media_final = round((semestre_1 + semestre_2) / 2.0, 2)
        situacao = "Aprovado" if media_final >= 6.0 else "Reprovado"

        alunos_limpos.append({
            "ra": ra,
            "nome": nome,
            "media": f"{media_final:.2f}",
            "situacao": situacao
        })

    # Mostra os 3 primeiros registros para conferência
    print("--- Prévia dos 3 primeiros alunos tratados ---")
    for aluno in alunos_limpos[:3]:
        print(aluno)
    
    print(f"\nTotal de alunos tratados com sucesso: {len(alunos_limpos)}")

if __name__ == "__main__":
    processar()