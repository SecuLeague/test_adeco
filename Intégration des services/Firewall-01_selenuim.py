from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.page_load_strategy = 'eager'
    
    # Configuration du service avec timeout augmenté
    service = Service(ChromeDriverManager().install())
    service.start()
    
    # Initialisation du driver avec des timeouts plus longs
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(180)  # Augmentation du timeout à 180 secondes
    driver.implicitly_wait(60)  # Attente implicite de 60 secondes
    
    # Navigation avec wait explicite
    wait = WebDriverWait(driver, 60)  # Attente explicite de 60 secondes
    driver.get('http://localhost:47743')
    
    print("Navigation réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
