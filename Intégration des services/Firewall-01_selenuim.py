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
    options.add_argument('--page-load-strategy=normal')
    options.add_argument('--window-size=1920,1080')
    options.page_load_strategy = 'eager'

    # Configuration du service avec timeout augmenté
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Augmentation des timeouts
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(20)
    
    # Navigation vers l'URL
    driver.get('http://172.16.100.1:4444')
    
    print("Navigation réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
