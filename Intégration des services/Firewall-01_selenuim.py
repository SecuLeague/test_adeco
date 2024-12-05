from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import traceback

def check_server_availability(driver, url, timeout=10):
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        return True
    except (TimeoutException, WebDriverException):
        return False

def main():
    url = 'http://172.16.150.2/'  # URL à vérifier
    
    options = Options()
    options.add_argument('-headless')
    
    service = Service('path/to/geckodriver')  # Remplacez par le chemin vers votre geckodriver
    
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
