from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('detach', True)
    
    # Configuration du service
    service = Service(ChromeDriverManager().install())
    
    # Création du driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(20)
    
    # Navigation avec pause
    driver.get('http://172.16.150.2')
    time.sleep(2)
    
    # Attente explicite des éléments
    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Username']")))
    password = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
    
    # Remplir les champs avec pause
    username.send_keys("admin")
    time.sleep(1)
    password.send_keys("pfsense")
    time.sleep(1)
    
    # Cliquer sur le bouton
    sign_in = driver.find_element(By.CSS_SELECTOR, "button.btn")
    sign_in.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
