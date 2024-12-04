import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests

def check_server_availability(url, timeout=5):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

try:
    # Vérifier la disponibilité du serveur
    if not check_server_availability('http://172.16.150.2'):
        print("Le serveur n'est pas accessible. Vérifiez votre connexion réseau.")
        exit(1)

    # Exécution de la commande cURL avec un timeout plus long
    curl_command = ["curl", "-v", "--connect-timeout", "30", "http://172.16.150.2/"]
    curl_output = subprocess.run(curl_command, capture_output=True, text=True, timeout=35)
    print("Sortie cURL:")
    print(curl_output.stdout)
    print(curl_output.stderr)

    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Configuration du service avec installation automatique
    service = Service(ChromeDriverManager().install())
    
    # Création du driver avec un timeout plus long
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)  # Augmentation du timeout à 60 secondes
    
    # Navigation vers pfSense
    driver.get('http://172.16.150.2')
    
    # Attente des éléments avec un timeout plus long
    wait = WebDriverWait(driver, 30)  # Augmentation du timeout à 30 secondes
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Username']")))
    password = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Password']")
    
    # Remplir les champs
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton SIGN IN
    sign_in = driver.find_element(By.CSS_SELECTOR, "button.btn")
    sign_in.click()
    
    # Attendre que la page soit chargée après la connexion
    wait.until(EC.url_changes('http://172.16.150.2'))
    
    print("Connexion réussie")

except subprocess.TimeoutExpired:
    print("La commande cURL a dépassé le délai d'attente.")
except Exception as e:
    print(f"Une erreur s'est produite : {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
