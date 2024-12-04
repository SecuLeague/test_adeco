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

def check_server_availability(url, timeout=30):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            if response.status_code == 200:
                return True
            time.sleep(5)  # Attendre 5 secondes entre les tentatives
        except requests.RequestException as e:
            print(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return False

def main():
    try:
        # Vérifier la disponibilité du serveur avec plusieurs tentatives
        print("Vérification de la disponibilité du serveur...")
        if not check_server_availability('http://172.16.150.2', timeout=30):
            print("Le serveur n'est pas accessible après plusieurs tentatives. Vérifiez votre connexion réseau.")
            return

        # Configuration des options Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--remote-debugging-port=9222')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        # Configuration du service avec installation automatique
        service = Service(ChromeDriverManager().install())
        
        # Création du driver avec un timeout plus long
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)
        
        # Navigation vers pfSense
        print("Tentative de connexion à pfSense...")
        driver.get('http://172.16.150.2')
        
        # Attente des éléments avec un timeout plus long
        wait = WebDriverWait(driver, 30)
        username = wait.until(EC.presence_of_element_located((By.ID, "usernamefld")))
        password = driver.find_element(By.ID, "passwordfld")
        
        # Remplir les champs
        username.send_keys("admin")
        password.send_keys("pfsense")
        
        # Cliquer sur le bouton SIGN IN
        sign_in = driver.find_element(By.NAME, "login")
        sign_in.click()
        
        # Attendre que la page soit chargée après la connexion
        wait.until(EC.url_changes('http://172.16.150.2'))
        
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
