from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


drive = webdriver.Chrome()
drive.get("https://www.harrypotter.com/pt/login")

drive.implicitly_wait(30)
email = drive.find_element(By.ID, "emailAddress")
email.send_keys("guleesin@gmail.com")
drive.find_element(By.ID, "password").send_keys("Harry@2026")
drive.find_element(By.XPATH, '//*[@data-testid="loginButton"]').click()
sleep(50)