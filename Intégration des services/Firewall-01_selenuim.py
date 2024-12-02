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
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=0')
    
    # Installation et configuration du service
    service = Service(ChromeDriverManager().install())
    
    # Création du driver
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)
    
    # Navigation vers pfSense
    driver.get('http://172.16.150.2')
    
    # Attente des éléments avec les bons sélecteurs
    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.presence_of_element_located((By.ID, "Username")))
    password = driver.find_element(By.ID, "Password")
    
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
