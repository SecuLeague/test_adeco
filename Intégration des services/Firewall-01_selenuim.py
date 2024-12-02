from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    
    # Configuration du service avec timeout augmenté
    service = Service(ChromeDriverManager().install())
    service.start()
    
    # Création du driver avec timeout personnalisé
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(300)  # Augmentation du timeout à 300 secondes
    
    # Navigation avec WebDriverWait
    driver.get('http://172.16.150.2/')
    
    # Attente explicite des éléments
    wait = WebDriverWait(driver, 30)
    username = wait.until(EC.presence_of_element_located((By.ID, "usernamefld")))
    password = driver.find_element(By.ID, "passwordfld")
    
    # Remplir les champs
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton login
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
