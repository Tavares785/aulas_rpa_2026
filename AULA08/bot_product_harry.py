from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
actions = ActionChains(driver)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
driver.get("https://www.harrypotter.com/pt/login")

SEL_PRODUTO = ".card__heading .full-unstyled-link"
SEL_PRECO = ".price-item--regular"

wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Harry Potter Logo']"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "shop"))).click()
wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[5]/div/div/div/div/a/button/span" ))).click()
wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
botao = driver.find_elements(By.CLASS_NAME, 'header-new__details')
actions.move_to_element(botao[1]).perform()
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="shopify-section-sections--17855488360617__header_new_KDWLMN"]/sticky-header/header/nav/ul/li[2]/header-menu/details/div/div/div/div[1]/ul/li[1]'))).click()
wait.until(EC.element_to_be_clickable((By.ID, "LoadMoreButton"))).click()
tabela = []
cards = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#product-grid > li"))
)
for card in cards:
    nome = card.find_element(By.CSS_SELECTOR, SEL_PRODUTO).text.strip()
    preco = card.find_element(By.CSS_SELECTOR, SEL_PRECO).text.strip()
    tabela.append((nome, preco))
print(tabela)