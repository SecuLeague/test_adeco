from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import subprocess

try:
    # Installation de Chrome et chromedriver si nécessaire
    subprocess.run(['sudo', 'apt-get', 'update'])
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'chromium-chromedriver'])
    
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Configuration du service avec chemin explicite vers chromedriver
    service = Service('/usr/lib/chromium-browser/chromedriver')
    
    # Création du driver
    driver = webdriver.Chrome(service=service, options=options)
    
    # Navigation vers pfSense
    driver.get('http://172.16.150.2')
    
    # Attente des éléments avec les bons sélecteurs
    wait = WebDriverWait(driver, 10)
    username = wait.until(EC.presence_of_element_located((By.ID, "usernamefld")))
    password = driver.find_element(By.ID, "passwordfld")
    
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    sign_in = driver.find_element(By.CLASS_NAME, "btn")
    sign_in.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
