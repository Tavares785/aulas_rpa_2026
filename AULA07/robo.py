import csv
import time
import pyautogui



# Configura uma pausa para não travar
pyautogui.PAUSE = 0.5



# Limpar a formatação das notas da planilha de notas
def limpar_nota(valor):
  if not valor:
    return 0.0
  # Tira espaços nas pontas, deixa tudo minúsculo e troca vírgula por ponto (para o Python conseguir somar)
  valor = valor.strip().lower().replace(',', '.')

  # Se o aluno faltou ou está sem nota, vira zero
  if valor in ['faltou', 'falta', 'n/a', '-', '']:
    return 0.0

  try:
    numero = float(valor)
    # Corrige erros de digitação onde a nota passou de 10
    if numero > 10.0:
      numero = 10.0
    return numero
  except ValueError:
    return 0.0



# Ler os dados
diario_classe = []

with open('notas_alunos.csv', mode='r', encoding='utf-8') as arquivo:
  leitor = csv.DictReader(arquivo, delimiter=';')

  for linha in leitor:
    # Limpa o nome (tira espaços extras e coloca iniciais maiúsculas)
    nome_limpo = ' '.join(linha['Nome'].split()).title()
    ra_limpo = linha['RA'].strip() if linha['RA'] else 'Sem RA'

    n1 = limpar_nota(linha['Nota01'])
    tf1 = limpar_nota(linha['TF01'])
    n2 = limpar_nota(linha['Nota02'])
    tf2 = limpar_nota(linha['TF02'])

    # Cálculo com Pesos (Nota peso 8, TF peso 2 -> divididos por 10)
    media_1 = (n1 * 8 + tf1 * 2) / 10
    media_2 = (n2 * 8 + tf2 * 2) / 10
    nota_final = round((media_1 + media_2) / 2, 2)

    situacao = 'Aprovado' if nota_final >= 7.0 else 'Reprovado'

    # Guarda o dicionário do aluno convertendo o ponto de volta para VÍRGULA (padrão brasileiro)
    diario_classe.append({
        'nome': nome_limpo,
        'ra': ra_limpo,
        'nota01': str(n1).replace('.', ','),
        'tf01': str(tf1).replace('.', ','),
        'nota02': str(n2).replace('.', ','),
        'tf02': str(tf2).replace('.', ','),
        'nota_final': nota_final,
        'situacao': situacao,
    })



total_alunos = len(diario_classe)
aprovados = sum(1 for a in diario_classe if a['situacao'] == 'Aprovado')
reprovados = total_alunos - aprovados
media_turma = sum(a['nota_final'] for a in diario_classe) / total_alunos


print('=' * 40)
print('📊 ESTATÍSTICAS DA TURMA')
print(f'Total de Alunos processados: {total_alunos}')
print(f'Aprovados: {aprovados} | Reprovados: {reprovados}')
print(f"Média Geral da Turma: {f'{media_turma:.2f}'.replace('.', ',')}")
print('=' * 40)


# Automação
print(
    '\n⚠️ ATENÇÃO: Abra a tela do Google Forms! O robô vai começar em 5'
    ' segundos...'
)
time.sleep(5)


# Suas coordenadas aqui!
X_CAMPO_NOME = 1580
Y_CAMPO_NOME = 440


# Rodando todos os alunos da planilha de notas
for indice, aluno in enumerate(diario_classe, start=1):
  print(f"Preenchendo aluno {indice}/{total_alunos}: {aluno['nome']}...")

  # 1. Clica no primeiro campo (Nome) do Google Forms
  pyautogui.click(x=X_CAMPO_NOME, y=Y_CAMPO_NOME)

  # 2. Digita o Nome e aperta TAB para ir para Nota 01
  pyautogui.write(aluno['nome'])
  pyautogui.press('tab')

  # 3. Digita Nota 01 e vai para TF 01
  pyautogui.write(aluno['nota01'])
  pyautogui.press('tab')

  # 4. Digita TF 01 e vai para Nota 02
  pyautogui.write(aluno['tf01'])
  pyautogui.press('tab')

  # 5. Digita Nota 02 e vai para TF 02
  pyautogui.write(aluno['nota02'])
  pyautogui.press('tab')

  # 6. Digita TF 02 e vai para o botão Enviar
  pyautogui.write(aluno['tf02'])
  pyautogui.press('tab')

  # 7. Aperta Enter para enviar o formulário
  pyautogui.press('enter')

  # 8. Espera 2 segundos para a página carregar a tela de confirmação
  time.sleep(2.0)

  # 9. No Google Forms, apertar TAB e depois ENTER na tela final clica em "Enviar outra resposta"!
  pyautogui.press('tab')
  pyautogui.press('enter')

  # Espera o formulário limpo recarregar antes de passar para o próximo aluno
  time.sleep(2.0)


print('✅ Automação concluída com sucesso!')
