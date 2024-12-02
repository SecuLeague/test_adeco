from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Installation et configuration du ChromeDriver
    service = Service(ChromeDriverManager(version="latest").install())
    
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Création du driver avec le service configuré
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(300)
    
    # Navigation vers pfSense
    driver.get('http://172.16.150.2')
    
    # Attente des éléments
    wait = WebDriverWait(driver, 30)
    username = wait.until(EC.presence_of_element_located((By.NAME, "usernamefld")))
    password = driver.find_element(By.NAME, "passwordfld")
    
    # Remplir les champs
    username.send_keys("admin")
    password.send_keys("pfsense")
    
    # Cliquer sur le bouton
    login_button = driver.find_element(By.CLASS_NAME, "btn")
    login_button.click()
    
    print("Connexion réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
