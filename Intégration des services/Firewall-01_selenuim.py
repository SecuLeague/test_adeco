from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('w3c', False)
    
    # Configuration du service
    service = Service()
    service.start()
    
    # Création du driver avec timeout augmenté
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    
    # Navigation avec retry
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get('http://172.16.150.2')
            break
        except:
            if attempt == max_retries - 1:
                raise
            time.sleep(5)
    
    # Attente des éléments avec les bons sélecteurs visibles dans l'image
    wait = WebDriverWait(driver, 20)
    username = wait.until(EC.presence_of_element_located((By.ID, "usernamefld")))
    password = driver.find_element(By.ID, "passwordfld")
    
    # Remplir les champs
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton SIGN IN
    sign_in = driver.find_element(By.CSS_SELECTOR, "button.btn")
    sign_in.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
