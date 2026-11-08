# lab 09 - web avancado
# Isabela - vou testar selects, alerts, iframe e abas

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# meu RA e nome pra usar no prompt e no iframe
meu_ra = "6326167"
meu_nome = "Isabela Maciel Coelho"

# pra nao ficar repetindo WebDriverWait toda hora
driver = webdriver.Chrome()
espera = WebDriverWait(driver, 10)

def parte_1_selects():
    print("parte 1 - selects")
    driver.get("https://the-internet.herokuapp.com/dropdown")

    # achei o dropdown pelo id
    caixinha = espera.until(EC.presence_of_element_located((By.ID, "dropdown")))
    select = Select(caixinha)

    # mostrar as opcoes que tem
    for opcao in select.options:
        print(opcao.text)

    # escolhi a option 2 pelo indice, indice 2
    select.select_by_index(2)

    # conferindo se foi mesmo
    assert select.first_selected_option.text == "Option 2"
    print("deu certo, ta na option 2")

def parte_2_alerts():
    print("parte 2 - alerts")
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    # 1 - alert normal, so clica em ok
    driver.find_element(By.XPATH, "//button[text()='Click for JS Alert']").click()
    alerta = espera.until(EC.alert_is_present())
    print("texto do alert:", alerta.text)
    alerta.accept()
    resultado = driver.find_element(By.ID, "result").text
    print(resultado)
    assert "You successfully clicked an alert" in resultado

    # 2 - confirm, aqui eu cancelei
    driver.find_element(By.XPATH, "//button[text()='Click for JS Confirm']").click()
    alerta = espera.until(EC.alert_is_present())
    print("texto do confirm:", alerta.text)
    alerta.dismiss() # dismiss = cancelar
    resultado = driver.find_element(By.ID, "result").text
    print(resultado)
    assert "You clicked: Cancel" in resultado

    # 3 - prompt, aqui digita o RA
    driver.find_element(By.XPATH, "//button[text()='Click for JS Prompt']").click()
    alerta = espera.until(EC.alert_is_present())
    alerta.send_keys(meu_ra)
    alerta.accept()
    resultado = driver.find_element(By.ID, "result").text
    print(resultado)
    assert meu_ra in resultado

def parte_3_iframes():
    print("parte 3 - iframe")
    driver.get("https://the-internet.herokuapp.com/iframe")

    # entra dentro do iframe pelo css, nao pelo id
    espera.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "div.tox-edit-area > iframe")))

    # acha o corpo do editor, apaga tudo e escreve
    corpo = espera.until(EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce")))
    corpo.click()
    corpo.send_keys(Keys.CONTROL + "a")
    corpo.send_keys(Keys.DELETE)
    corpo.send_keys(f"Meu RA e {meu_ra} e meu nome e {meu_nome}")

    # volta pro documento normal
    driver.switch_to.default_content()

    # pega o titulo h3 pra provar que voltou
    titulo = driver.find_element(By.TAG_NAME, "h3").text
    print("titulo:", titulo)

def parte_4_abas():
    print("parte 4 - abas")
    driver.get("https://the-internet.herokuapp.com/windows")

    # salva qual e a aba original
    aba_original = driver.current_window_handle
    titulo_original = driver.title

    driver.find_element(By.LINK_TEXT, "Click Here").click()

    # espera abrir a segunda aba
    espera.until(EC.number_of_windows_to_be(2))
    assert len(driver.window_handles) == 2

    # troca pra aba que nao e a original
    for aba in driver.window_handles:
        if aba != aba_original:
            driver.switch_to.window(aba)
            break

    titulo_novo = driver.find_element(By.TAG_NAME, "h3").text
    print("nova aba:", titulo_novo)
    assert "New Window" in titulo_novo

    # fecha a nova e volta
    driver.close()
    driver.switch_to.window(aba_original)

    assert driver.title == titulo_original
    print("voltei pra aba original:", driver.title)

# roda tudo
try:
    parte_1_selects()
    parte_2_alerts()
    parte_3_iframes()
    parte_4_abas()
    print("terminei tudo!")
finally:
    driver.quit()
