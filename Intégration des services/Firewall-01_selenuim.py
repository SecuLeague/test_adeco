from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # Configuration du service
    service = Service('/usr/bin/chromedriver')
    
    # Création du driver avec timeout augmenté
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(300)  # Timeout augmenté à 300 secondes
    
    # Configuration du WebDriverWait avec timeout augmenté
    wait = WebDriverWait(driver, 300)  # Timeout d'attente augmenté à 300 secondes
    
    # Navigation
    driver.get('http://172.16.150.2')
    
    # Attente des éléments avec le nouveau timeout
    username = wait.until(EC.presence_of_element_located((By.NAME, "usernamefld")))
    password = driver.find_element(By.NAME, "passwordfld")
    
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    login_button = driver.find_element(By.CLASS_NAME, "btn")
    login_button.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
