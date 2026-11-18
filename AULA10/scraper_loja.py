import csv
import os
import time
from bs4 import BeautifulSoup

# Tenta usar curl_cffi (burla bloqueio 429 de TLS da Shopify); se não houver, usa requests
try:
    from curl_cffi import requests as req_lib
    USANDO_CFFI = True
except ImportError:
    import requests as req_lib
    USANDO_CFFI = False

url = "https://harrypottershop.co.uk/collections/gryffindor"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en;q=0.9"
}

if USANDO_CFFI:
    resposta = req_lib.get(url, impersonate="chrome", headers=headers)
else:
    resposta = req_lib.get(url, headers=headers)

if resposta.status_code == 200:
    print("Conexão realizada com sucesso! Extraindo dados...\n")
    
    soup = BeautifulSoup(resposta.text, "html.parser")
    produtos_extraidos = []
    cards = soup.select(".card")
    
    for card in cards:
        elemento_nome = card.select_one(".card__heading")
        
        elemento_preco = card.select_one(".price-item--sale")
        if not elemento_preco:
            elemento_preco = card.select_one(".price-item--regular")
            
        if elemento_nome and elemento_preco:
            nome_limpo = " ".join(elemento_nome.get_text().split())
            preco_limpo = " ".join(elemento_preco.get_text().split())
            
            produtos_extraidos.append({
                "nome": nome_limpo,
                "preco": preco_limpo
            })
            
    print("--- TOP 5 PRODUTOS DA GRIFINÓRIA ---")
    for item in produtos_extraidos[:5]:
        print(f"Produto: {item['nome']} | Preço: {item['preco']}")
        
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(pasta_script, "produtos_gryffindor.csv")
    
    with open(caminho_csv, mode="w", newline="", encoding="utf-8") as arquivo_csv:
        colunas = ["nome", "preco"]
        escritor = csv.DictWriter(arquivo_csv, fieldnames=colunas)
        
        escritor.writeheader()
        escritor.writerows(produtos_extraidos)
        
    print(f"\nSucesso! {len(produtos_extraidos)} produtos salvos em '{caminho_csv}'.")

else:
    print(f"Erro ao acessar a página. Código HTTP: {resposta.status_code}")