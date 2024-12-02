from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Configuration des options Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    # Ajout de ces options pour résoudre le problème de crash
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    
    # Configuration du service avec le chemin explicite vers Chrome
    service = Service(ChromeDriverManager().install())
    service.start()
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # Navigation vers l'URL
    driver.get('http://172.16.150.2/')
    print("Navigation réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
