from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # Mode sans interface graphique
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--remote-debugging-port=9222')

    # Installation et configuration du service Chrome
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Configuration du timeout
    driver.set_page_load_timeout(30)
    
    # Navigation vers l'URL
    driver.get('http://172.16.100.1:4444')
    
    # Attendre que la page soit chargée
    driver.implicitly_wait(10)
    
    print("Navigation réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    # Fermeture propre du driver
    if 'driver' in locals():
        driver.quit()
