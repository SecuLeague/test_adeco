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
from chromedriver_py import binary_path

def check_server_availability(url, timeout=30):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            if response.status_code == 200:
                return True
            else:
                print(f"Erreur HTTP : {response.status_code}")
        except requests.RequestException as e:
            print(f"Tentative {attempt + 1}/{max_retries} échouée : {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    return False

def main():
    url = 'https://www.seculeague.link'
    
    # Vérification de la disponibilité du serveur avec curl
    print("Vérification de la disponibilité du serveur avec curl...")
    
    if not check_server_availability(url):
        print("Le serveur n'est pas disponible. Arrêt du script.")
        return

    try:
        print("Vérification de la disponibilité du serveur avec Selenium...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        svc = webdriver.ChromeService(executable_path=binary_path)
        
        driver = webdriver.Chrome(service=svc, options=options)
        
        driver.implicitly_wait(30)
        driver.set_page_load_timeout(60)
        driver.set_script_timeout(30)
        
        print("Tentative de connexion à pfSense...")
        driver.get(url)
        
        wait = WebDriverWait(driver, 60)
        
        try:
            cred_login = wait.until(EC.presence_of_element_located((By.NAME, "credloginbutton")))
            cred_login.click()
            time.sleep(2)
        except:
            pass

        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        username.clear()
        username.send_keys("admin")
        password.clear()
        password.send_keys("pfsense")
        
        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "loginbutton")))
        login_button.click()
        
        wait.until(EC.url_changes(url))
        
        print("Connexion réussie")

        input("Appuyez sur une touche pour quitter.")

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        print("Traceback complet:")
        traceback.print_exc()
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
