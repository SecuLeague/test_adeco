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
    
    # Configuration du service avec installation automatique du driver
    service = Service(ChromeDriverManager().install())
    
    # Création du driver
    driver = webdriver.Chrome(service=service, options=options)
    
    # Navigation vers pfSense
    driver.get('http://172.16.150.2')
    
    # Attente des éléments avec les bons sélecteurs visibles dans l'image
    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.presence_of_element_located((By.NAME, "Username")))
    password = driver.find_element(By.NAME, "Password")
    
    # Remplir les champs
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton vert SIGN IN
    sign_in = driver.find_element(By.CSS_SELECTOR, "button.btn")
    sign_in.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
