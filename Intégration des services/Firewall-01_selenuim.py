from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    
    # Configuration du service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Configuration des timeouts
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    
    # Navigation vers l'URL avec gestion d'erreur réseau
    try:
        driver.get('http://172.16.150.2/')
        
        # Attendre que les éléments soient chargés
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "usernamefld"))
        )
        password = driver.find_element(By.NAME, "passwordfld")
        
        # Remplir les champs
        username.send_keys("admin")  # Remplacer par votre nom d'utilisateur
        password.send_keys("pfsense")  # Remplacer par votre mot de passe
        
        # Cliquer sur le bouton de connexion
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        
        print("Navigation et connexion réussies")
        
    except Exception as e:
        print(f"Erreur de connexion au serveur: {str(e)}")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
