import requests
from bs4 import BeautifulSoup
import csv

url = "https://harrypottershop.co.uk/collections/gryffindor"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    produtos = []
    
    cards = soup.select('.card')
    
    for card in cards:
        nome_elem = card.select_one('.card__heading')
        nome = nome_elem.get_text(strip=True) if nome_elem else "Nome não encontrado"
        
        preco_elem = card.select_one('.price-item--sale') or card.select_one('.price-item--regular') or card.select_one('.price-item')
        preco = preco_elem.get_text(strip=True) if preco_elem else "Preço não encontrado"
        
        if nome != "Nome não encontrado":
            produtos.append({"nome": nome, "preco": preco})
    
    print("--- 5 PRIMEIROS PRODUTOS ---")
    for p in produtos[:5]:
        print(f"Nome: {p['nome']} | Preço: {p['preco']}")
    
    with open("produtos_gryffindor.csv", mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nome", "preco"])
        writer.writeheader()
        writer.writerows(produtos)
    print("\nArquivo 'produtos_gryffindor.csv' gerado com sucesso!")
else:
    print(f"Erro ao acessar a página: {response.status_code}")
