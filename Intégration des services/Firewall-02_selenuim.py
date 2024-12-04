import asyncio
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import traceback

async def check_server_availability(url):
    try:
        # Utiliser curl pour vérifier la disponibilité du serveur avec -k pour ignorer les erreurs SSL
        result = subprocess.run(['curl', '-k', '-o', '/dev/null', '-s', '-w', '%{http_code}', url], capture_output=True, text=True)
        return result.stdout == '200'
    except Exception as e:
        print(f"Erreur lors de l'exécution de curl : {str(e)}")
        return False

async def main():
    try:
        print("Vérification de la disponibilité du serveur...")
        
        if not await check_server_availability('https://172.16.150.1:4444/'):
            print("Le serveur n'est pas accessible. Vérifiez votre connexion réseau.")
            return

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        
        print("Tentative de connexion à pfSense...")
        driver.get('https://172.16.150.1:4444/')
        
        wait = WebDriverWait(driver, 30)
        
        try:
            cred_login = wait.until(EC.presence_of_element_located((By.NAME, "credloginbutton")))
            cred_login.click()
        except:
            pass

        username = wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = wait.until(EC.presence_of_element_located((By.ID, "password")))
        
        username.clear()
        username.send_keys("admin")
        password.clear()
        password.send_keys("sophos")  # Mot de passe modifié ici
        
        login_button = wait.until(EC.element_to_be_clickable((By.NAME, "loginbutton")))
        login_button.click()
        
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
    asyncio.run(main())
