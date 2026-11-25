import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

LINK = "https://docs.google.com/forms/d/e/1FAIpQLSeB2LE3y0qfd22q_6KV7QEnpMGkyQEe-2K6HZ2IDTFioe5QXA/viewform?usp=dialog"

# Abre o Chrome sozinho
driver = webdriver.Chrome()
driver.get(LINK)
time.sleep(3)

with open("notas.csv", encoding="utf-8") as f:
    linhas = list(csv.reader(f))
    cabecalho = linhas[0]
    dados = linhas[1:]
    
print("Colunas do seu arquivo:", cabecalho)
print(f"Vou preencher {len(dados)} alunos")

for linha in dados:
    # Preenche tudo que achar por ordem
    campos = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='number']")
    
    for i, valor in enumerate(linha):
        if i < len(campos):
            campos[i].clear()
            campos[i].send_keys(valor)
            time.sleep(0.3)
    
    # Clica em Enviar
    time.sleep(1)
    driver.find_element(By.XPATH, "//span[text()='Enviar']").click()
    time.sleep(3)
    
    # Clica em "Enviar outra resposta"
    try:
        driver.find_element(By.XPATH, "//a[contains(text(),'Enviar outra')]").click()
    except:
        driver.get(LINK)
    time.sleep(3)

print("Acabou!")