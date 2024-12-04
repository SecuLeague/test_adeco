import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import traceback
import time
from selenium.webdriver.common.keys import Keys

def check_server_availability(url, timeout=30):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            return True
        except requests.RequestException as e:
            print(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return False

def main():
    try:
        print("Vérification de la disponibilité du serveur...")
        
        # Exécution de la commande curl
        curl_command = "curl -k -u admin https://172.16.150.1:4444/"
        curl_process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        curl_output, curl_error = curl_process.communicate()
        
        print("Résultat de la commande curl:")
        print(curl_output.decode())
        
        if curl_error:
            print("Erreur curl:")
            print(curl_error.decode())
        
        # Configuration des options Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Configuration du service avec installation automatique
        service = Service(ChromeDriverManager().install())
        
        # Création du driver avec un timeout plus long
        driver = webdriver.Chrome(service=service, options=options)
        
        # Augmenter le timeout implicite
        driver.implicitly_wait(30)

        # Augmenter le timeout de chargement de page
        driver.set_page_load_timeout(60)

        # Augmenter le timeout de script
        driver.set_script_timeout(30)
        
        # Navigation vers pfSense
        print("Tentative de connexion à pfSense...")
        driver.get('https://172.16.150.1:4444/')
        
        # Utiliser un wait explicite avec un timeout plus long
        wait = WebDriverWait(driver, 60)
        
        # Cliquer sur le bouton "Credential Login" s'il existe
        try:
            cred_login = wait.until(EC.presence_of_element_located((By.NAME, "credloginbutton")))
            cred_login.click()
            time.sleep(2)
        except:
            pass

        # Attendre et remplir les champs de connexion
        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        # Effacer et remplir les champs
        username.clear()
        username.send_keys("admin")
        password.clear()
        password.send_keys("pfsense")
        
        # Cliquer sur le bouton Login
        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "loginbutton")))
        login_button.click()
        
        # Attendre la redirection
        wait.until(EC.url_changes('https://172.16.150.1:4444/'))
        
        print("Connexion réussie")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        print("Traceback complet:")
        traceback.print_exc()
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
