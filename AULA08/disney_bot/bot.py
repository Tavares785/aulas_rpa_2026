from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
print("Abrindo o site da Disney...")
driver.get("https://www.disney.com.br/filmes")
driver.maximize_window()
time.sleep(6)

print("Coletando filmes...")

imagens = driver.find_elements(By.CSS_SELECTOR, "img[alt]")
filmes_encontrados = []

for filme in imagens:
    nome = filme.get_attribute("alt")
    if nome and len(nome) > 3:
        print(f" - {nome}")
        filmes_encontrados.append(nome)

# A PARTE QUE FALTAVA - SALVAR NO ARQUIVO
print(f"\nSalvando {len(filmes_encontrados)} filmes no filmes.txt...")
with open("filmes.txt", "w", encoding="utf-8") as arquivo:
    for nome in filmes_encontrados:
        arquivo.write(nome + "\n")

print("\nPronto!")
driver.quit()