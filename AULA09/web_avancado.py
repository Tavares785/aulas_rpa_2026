import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    datefmt="%H:%M:%S",
)

RA = "6326085"


def parte_1_selects(driver):
  logging.info("Iniciando Parte 1: Selects")
  driver.get("https://the-internet.herokuapp.com/dropdown")

  wait = WebDriverWait(driver, 10)
  select_element = wait.until(
      EC.presence_of_element_located((By.ID, "dropdown"))
  )
  select = Select(select_element)

  options = select.options
  logging.info("Opções disponíveis no dropdown:")
  for opt in options:
    logging.info(f" - {opt.text}")

  select.select_by_index(2)
  logging.info("Selecionada a opção correspondente ao índice 2.")

  selected_text = select.first_selected_option.text
  assert (
      selected_text == "Option 2"
  ), f"Erro: Esperado 'Option 2', mas obtido '{selected_text}'"
  logging.info(
      f"Validação da Parte 1 bem-sucedida: Option selecionada -> {selected_text}"
  )


def parte_2_alerts(driver):
  logging.info("Iniciando Parte 2: JavaScript Alerts")
  driver.get("https://the-internet.herokuapp.com/javascript_alerts")
  wait = WebDriverWait(driver, 10)

  btn_alert = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//button[contains(text(), 'Click for JS Alert')]")
      )
  )
  btn_alert.click()
  alert = wait.until(EC.alert_is_present())
  alert_text = alert.text
  logging.info(f"Alerta JS capturado com texto: '{alert_text}'")
  alert.accept()
  assert (
      "I am a JS Alert" in alert_text
  ), f"Texto do alerta inesperado: {alert_text}"

  btn_confirm = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//button[contains(text(), 'Click for JS Confirm')]")
      )
  )
  btn_confirm.click()
  alert = wait.until(EC.alert_is_present())
  alert.dismiss()
  logging.info("JS Confirm acionado e cancelado com dismiss().")

  result_element = wait.until(
      EC.presence_of_element_located((By.ID, "result"))
  )
  result_text = result_element.text
  assert (
      "You clicked: Cancel" in result_text
  ), f"Esperado indicador de cancelamento, obtido: '{result_text}'"
  logging.info(f"Validação do JS Confirm concluída: '{result_text}'")

  btn_prompt = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//button[contains(text(), 'Click for JS Prompt')]")
      )
  )
  btn_prompt.click()
  alert = wait.until(EC.alert_is_present())
  logging.info(f"Enviando o RA {RA} para o prompt...")
  alert.send_keys(RA)
  alert.accept()

  result_element = wait.until(
      EC.visibility_of_element_located((By.ID, "result"))
  )
  result_text = result_element.text
  assert (
      RA in result_text
  ), f"Erro: O RA {RA} não foi encontrado no resultado: '{result_text}'"
  logging.info(f"Validação do JS Prompt concluída com sucesso: '{result_text}'")


def parte_3_iframes(driver):
  logging.info("Iniciando Parte 3: Iframes")
  driver.get("https://the-internet.herokuapp.com/iframe")
  wait = WebDriverWait(driver, 10)

  iframe_element = wait.until(
      EC.presence_of_element_located(
          (By.CSS_SELECTOR, "div.tox-edit-area iframe, iframe")
      )
  )
  driver.switch_to.frame(iframe_element)
  logging.info("Foco alternado para o iframe com sucesso.")

  body_element = wait.until(
      EC.presence_of_element_located((By.ID, "tinymce"))
  )
  body_element.clear()
  mensagem = f"Automação de Testes Web avançada concluída. RA: {RA}"
  body_element.send_keys(mensagem)
  logging.info(f"Mensagem inserida no editor: '{mensagem}'")

  driver.switch_to.default_content()
  logging.info("Foco retornado ao DOM raiz (default_content).")

  h3_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
  h3_text = h3_element.text
  assert (
      "Editor" in h3_text or "An iFrame" in h3_text
  ), f"Cabeçalho inesperado fora do iframe: '{h3_text}'"
  logging.info(f"Validação da Parte 3 concluída. Cabeçalho H3: '{h3_text}'")


def parte_4_janelas(driver):
  logging.info("Iniciando Parte 4: Troca de Abas / Janelas")
  driver.get("https://the-internet.herokuapp.com/windows")
  wait = WebDriverWait(driver, 10)

  handle_original = driver.current_window_handle
  logging.info(f"Handle original guardado: {handle_original}")

  link_click_here = wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//a[contains(text(), 'Click Here')]")
      )
  )
  link_click_here.click()
  logging.info("Link 'Click Here' acionado.")

  wait.until(EC.number_of_windows_to_be(2))
  handles = driver.window_handles
  logging.info(f"Total de janelas ativas detectadas: {len(handles)}")

  handle_novo = [h for h in handles if h != handle_original][0]
  driver.switch_to.window(handle_novo)
  logging.info("Foco alterado para a nova aba.")

  h3_new = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h3")))
  assert (
      h3_new.text == "New Window"
  ), f"Esperado 'New Window', obtido: '{h3_new.text}'"
  logging.info(f"Texto da nova aba validado com sucesso: '{h3_new.text}'")

  driver.close()
  logging.info("Nova aba fechada com driver.close().")
  driver.switch_to.window(handle_original)
  logging.info("Foco retornado para a aba original.")

  assert (
      len(driver.window_handles) == 1
  ), "Erro: Deveria existir apenas 1 handle ativo ao final."
  assert (
      "The Internet" in driver.title
  ), f"Título da página original incorreto: '{driver.title}'"
  logging.info(
      "Validação da Parte 4 concluída com sucesso: Retorno íntegro à aba"
      " original."
  )


def bonus_multiplas_janelas(driver):
  logging.info("Iniciando Bônus: Gerenciamento genérico de múltiplas janelas")
  driver.get("https://the-internet.herokuapp.com/windows")
  wait = WebDriverWait(driver, 10)

  handle_original = driver.current_window_handle

  wait.until(
      EC.element_to_be_clickable(
          (By.XPATH, "//a[contains(text(), 'Click Here')]")
      )
  ).click()
  wait.until(EC.number_of_windows_to_be(2))

  def processar_e_fechar_novas_abas(drv, handle_orig):
    todas_as_janelas = drv.window_handles
    logging.info(f"Iterando sobre {len(todas_as_janelas)} janelas abertas.")
    for h in todas_as_janelas:
      if h != handle_orig:
        drv.switch_to.window(h)
        titulo_aba = drv.title
        conteudo_aba = drv.find_element(By.TAG_NAME, "h3").text
        logging.info(
            f"Processando aba extra [Título: {titulo_aba} | Conteúdo:"
            f" {conteudo_aba}]"
        )
        drv.close()
        logging.info(f"Aba extra {h} fechada com segurança.")
    drv.switch_to.window(handle_orig)
    assert (
        len(drv.window_handles) == 1
    ), "Erro no bônus: Apenas a aba original deveria restar."
    logging.info("Retorno seguro à aba original garantido pelo bônus.")

  processar_e_fechar_novas_abas(driver, handle_original)


if __name__ == "__main__":
  options = Options()
  driver = webdriver.Chrome(options=options)
  try:
    parte_1_selects(driver)
    parte_2_alerts(driver)
    parte_3_iframes(driver)
    parte_4_janelas(driver)
    bonus_multiplas_janelas(driver)
    logging.info("🎉 Todas as partes do Lab 09 foram executadas com sucesso!")
  except Exception as e:
    logging.error(f"Ocorreu um erro crítico durante a execução: {e}")
    raise e
  finally:
    driver.quit()
    logging.info("Instância do WebDriver encerrada com sucesso no bloco finally.")