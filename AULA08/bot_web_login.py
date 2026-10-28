"""Robô de automação para login de teste no the-internet.herokuapp.com."""

from selenium import webdriver
from selenium.webdriver.common.by import By


def executar_login():
    """Acessa a página de login e preenche as credenciais de teste."""
    driver = webdriver.Chrome()
    try:
        driver.implicitly_wait(10)
        driver.get("https://the-internet.herokuapp.com/login")

        campo_usuario = driver.find_element(By.ID, "username")
        campo_usuario.send_keys("tomsmith")

        campo_senha = driver.find_element(By.ID, "password")
        campo_senha.send_keys("SuperSecretPassword!")

        botao_login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        botao_login.click()
    finally:
        driver.quit()


if __name__ == "__main__":
    executar_login()

