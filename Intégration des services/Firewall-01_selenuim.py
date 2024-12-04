import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    try:
        # Configuration des options Chrome
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        
        # Configuration du service
        service = Service(ChromeDriverManager().install())
        
        # Création du driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Navigation vers l'API pfSense
        print("Tentative de connexion à l'API pfSense...")
        driver.get('http://172.16.150.2/api/v1/')
        
        # Attente explicite
        wait = WebDriverWait(driver, 10)
        
        # Authentification Basic Auth
        username = "admin"
        password = "Seculeague2024"
        
        # Envoi de la requête avec l'authentification
        curl_command = [
            'curl',
            '-k',
            '-X', 'GET',
            '-u', f'{username}:{password}',
            'http://172.16.150.2/api/v1/'
        ]
        
        response = subprocess.run(curl_command, capture_output=True, text=True)
        print(response.stdout)

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()
