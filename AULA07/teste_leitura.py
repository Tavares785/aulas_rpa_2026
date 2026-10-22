with open("notas_alunos.csv", "r", encoding="utf-8") as f:
    linhas = f.readlines()

print(f"Total de linhas lidas (incluindo cabeçalho): {len(linhas)}")
print(f"Primeira linha: {linhas[0].strip()}")
print(f"Segunda linha: {linhas[1].strip()}")