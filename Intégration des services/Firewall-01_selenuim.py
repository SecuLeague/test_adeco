import os
import subprocess
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import traceback

def install_geckodriver():
    print("Installation de geckodriver...")
    try:
        subprocess.run("wget https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.33.0-linux64.tar.gz && "
                       "tar -xvzf geckodriver-v0.33.0-linux64.tar.gz && "
                       "chmod +x geckodriver && "
                       "sudo mv geckodriver /usr/local/bin/", shell=True, check=True)
        print("geckodriver installé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de geckodriver : {e}")
        print("Tentative d'installation avec curl...")
        try:
            subprocess.run("curl -L https://github.com/mozilla/geckodriver/releases/latest/download/geckodriver-v0.33.0-linux64.tar.gz | tar -xz && "
                           "chmod +x geckodriver && "
                           "sudo mv geckodriver /usr/local/bin/", shell=True, check=True)
            print("geckodriver installé avec succès en utilisant curl.")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation de geckodriver avec curl : {e}")
            raise

def check_server_availability(driver, url, timeout=10):
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        return True
    except (TimeoutException, WebDriverException):
        return False

def main():
    url = 'http://172.16.150.2/'  # URL à vérifier
    
    # Installer geckodriver si nécessaire
    if not os.path.exists('/usr/local/bin/geckodriver'):
        install_geckodriver()
    
    options = Options()
    options.add_argument('-headless')
    
    service = Service('/usr/local/bin/geckodriver')
    
    try:
        with webdriver.Firefox(service=service, options=options) as driver:
            print("Vérification de la disponibilité du serveur...")
            
            if not check_server_availability(driver, url):
                print("Le serveur n'est pas accessible. Vérifiez votre connexion réseau.")
                return
            
            print("Le serveur est accessible. Tentative d'accès à la page...")

            # Accéder à la page et afficher le contenu
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            content = driver.page_source
            print("Contenu de la page :")
            print(content[:500])  # Affiche les 500 premiers caractères du contenu

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        print("Traceback complet:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
