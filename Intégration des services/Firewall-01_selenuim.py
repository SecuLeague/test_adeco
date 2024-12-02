from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

try:
    # Configuration des options Chrome avec des paramètres plus stricts
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--window-size=1920,1080')
    
    # Configuration du service avec le chemin explicite
    service = Service()
    
    # Création du driver avec timeout augmenté
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(300)
    
    # Navigation vers pfSense
    driver.get('http://172.16.150.2')
    
    # Attente des éléments avec les bons sélecteurs
    wait = WebDriverWait(driver, 30)
    username = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
    password = driver.find_element(By.NAME, "Password")
    
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton SIGN IN
    sign_in = driver.find_element(By.CLASS_NAME, "btn")
    sign_in.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
