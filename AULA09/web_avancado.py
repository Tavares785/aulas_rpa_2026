import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

RA_ALUNO = "6326262"


def iniciar_driver():
  options = webdriver.ChromeOptions()

  driver = webdriver.Chrome(
      service=ChromeService(ChromeDriverManager().install()), options=options
  )
  driver.maximize_window()
  return driver


def parte_1_selects(driver):
  logging.info("Iniciando Parte 1: Selects")
  driver.get("https://the-internet.herokuapp.com/dropdown")

  wait = WebDriverWait(driver, 10)
  select_element = wait.until(
      EC.presence_of_element_located((By.ID, "dropdown"))
  )
  select = Select(select_element)

  for option in select.options:
    logging.info(f"Opção disponível no dropdown: {option.text}")

  select.select_by_index(2)

  assert (
      select.first_selected_option.text == "Option 2"
  ), "A opção selecionada não é a Opção 2!"
  logging.info("Parte 1 validada com sucesso: Option 2 selecionada.")


def parte_2_alerts(driver):
  logging.info("Iniciando Parte 2: Alertas JS")
  driver.get("https://the-internet.herokuapp.com/javascript_alerts")
  wait = WebDriverWait(driver, 10)

  botao_alerta = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//button[text()='Click for JS Alert']")
      )
  )
  botao_alerta.click()
  alert = wait.until(EC.alert_is_present())
  logging.info(f"Texto do Alerta 1: {alert.text}")
  alert.accept()

  botao_confirm = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//button[text()='Click for JS Confirm']")
      )
  )
  botao_confirm.click()
  alert = wait.until(EC.alert_is_present())
  alert.dismiss()
  resultado = driver.find_element(By.ID, "result").text
  assert (
      "Cancel" in resultado
  ), "O resultado do alerta cancelado não bateu com o esperado!"
  logging.info(f"Parte 2 (Confirm) validada. Resultado: {resultado}")


  botao_prompt = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//button[text()='Click for JS Prompt']")
      )
  )
  botao_prompt.click()
  alert = wait.until(EC.alert_is_present())
  alert.send_keys(RA_ALUNO)
  alert.accept()
  resultado_prompt = driver.find_element(By.ID, "result").text
  assert (
      RA_ALUNO in resultado_prompt
  ), f"O RA {RA_ALUNO} não apareceu no resultado!"
  logging.info(f"Parte 2 (Prompt) validada com sucesso. Texto: {resultado_prompt}")


def parte_3_iframes(driver):
  logging.info("Iniciando Parte 3: Iframes")
  driver.get("https://the-internet.herokuapp.com/iframe")
  wait = WebDriverWait(driver, 10)

  iframe_element = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.tox-edit-area__iframe, iframe#mce_0_ifr"))
)
  driver.switch_to.frame(iframe_element)

  corpo_editor = wait.until(
     EC.presence_of_element_located((By.CSS_SELECTOR, "body#tinymce"))
  )
  corpo_editor.clear()
  corpo_editor.send_keys(f"Automação realizada com sucesso pelo RA: {RA_ALUNO}")
  logging.info("Texto inserido dentro do Iframe.")

  driver.switch_to.default_content()

  cabecalho = wait.until(
      EC.visibility_of_element_located((By.TAG_NAME, "h3"))
  ).text
  assert (
      "An iFrame containing the TinyMCE WYSIWYG Editor" in cabecalho
  ), "Não retornou corretamente ao documento principal!"
  logging.info(f"Parte 3 validada com sucesso. Cabeçalho encontrado: {cabecalho}")


def parte_4_windows(driver):
  logging.info("Iniciando Parte 4: Troca de Abas")
  driver.get("https://the-internet.herokuapp.com/windows")
  wait = WebDriverWait(driver, 10)

  handle_original = driver.current_window_handle
  logging.info(f"Handle original salvo: {handle_original}")

  link_nova_aba = wait.until(
      EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
  )
  link_nova_aba.click()

  wait.until(EC.number_of_windows_to_be(2))

  handles = driver.window_handles
  nova_aba = [h for h in handles if h != handle_original][0]
  driver.switch_to.window(nova_aba)

  texto_nova_janela = wait.until(
      EC.visibility_of_element_located((By.TAG_NAME, "h3"))
  ).text
  assert (
      texto_nova_janela == "New Window"
  ), "O texto da nova janela não confere!"
  logging.info("Nova aba acessada e validada com sucesso.")

  driver.close()
  driver.switch_to.window(handle_original)

  assert len(driver.window_handles) == 1, "Deveria restar apenas 1 aba aberta!"
  assert (
      "The Internet" in driver.title
  ), "O título da página original não confere!"
  logging.info("Parte 4 concluída: retorno à aba original validado com sucesso.")


if __name__ == "__main__":
  driver = iniciar_driver()
  try:
    parte_1_selects(driver)
    parte_2_alerts(driver)
    parte_3_iframes(driver)
    parte_4_windows(driver)
    logging.info("TODAS AS PARTES FORAM EXECUTADAS COM SUCESSO!")
  except Exception as e:
    logging.error(f"Erro ocorrido durante a execução: {e}")
    raise e
  finally:
    driver.quit()
    logging.info("Driver encerrado com segurança.")