from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--dns-prefetch-disable')
    options.add_argument('--proxy-bypass-list=*')
    
    # Configuration du service
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Configuration des timeouts
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(10)
    
    # Navigation vers l'URL avec gestion d'erreur réseau
    try:
        driver.get('http://172.16.150.2/')
        print("Navigation réussie")
    except:
        print("Erreur de connexion au serveur")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
