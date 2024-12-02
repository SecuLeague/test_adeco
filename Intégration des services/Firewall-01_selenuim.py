from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.page_load_strategy = 'eager'  # Chargement plus rapide
    
    # Configuration du service
    service = Service(ChromeDriverManager().install())
    
    # Création du driver avec timeouts personnalisés
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    
    # Navigation avec retry
    driver.get('http://172.16.150.2')
    
    # Attente explicite des éléments avec timeout court
    wait = WebDriverWait(driver, 5)
    username = wait.until(EC.presence_of_element_located((By.NAME, "usernamefld")))
    password = driver.find_element(By.NAME, "passwordfld")
    
    # Remplir les champs
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton
    sign_in = driver.find_element(By.CLASS_NAME, "btn")
    sign_in.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
