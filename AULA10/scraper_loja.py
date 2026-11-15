
from bs4 import BeautifulSoup
import csv

# 1. Ler o arquivo TXT
try:
    with open("produtos.txt", "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.readlines()

    print("Arquivo carregado com sucesso!")

except FileNotFoundError:
    print("Erro: arquivo produtos.txt não encontrado!")
    exit()

# 2. Preparar o conteúdo para o BeautifulSoup
html = ""

for linha in conteudo:
    linha = linha.strip()

    if linha:
        nome, preco = linha.split(";")

        html += f"""
        <div class="product-card">
            <h2 class="product-name">{nome}</h2>
            <span class="price">{preco}</span>
        </div>
        """

# 3. Utilizar BeautifulSoup para interpretar o conteúdo
soup = BeautifulSoup(html, "html.parser")

# 4. Localizar todos os cards de produtos
cards = soup.find_all("div", class_="product-card")

produtos = []

# 5. Extrair nome e preço de cada produto
for card in cards:
    nome = card.find("h2", class_="product-name").get_text()
    preco = card.find("span", class_="price").get_text()

    # 6. Limpar espaços desnecessários
    nome = " ".join(nome.strip().split())
    preco = " ".join(preco.strip().split())

    produtos.append({
        "nome": nome,
        "preco": preco
    })

# 7. Exibir os 5 primeiros produtos
print("\n===== PRIMEIROS 5 PRODUTOS =====")

for produto in produtos[:5]:
    print(f"{produto['nome']} - {produto['preco']}")

# 8. Salvar todos os produtos em CSV
with open("produtos_gryffindor.csv", "w",
          newline="", encoding="utf-8") as arquivo:

    escritor = csv.DictWriter(
        arquivo,
        fieldnames=["nome", "preco"]
    )

    escritor.writeheader()
    escritor.writerows(produtos)

print("\nArquivo produtos_gryffindor.csv salvo com sucesso!")
