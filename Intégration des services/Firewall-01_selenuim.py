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
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    options.page_load_strategy = 'eager'
    
    # Configuration du service avec timeout augmenté
    service = Service(ChromeDriverManager().install())
    service.start()
    
    # Initialisation du driver avec des timeouts plus longs
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(30)
    
    # Navigation avec wait explicite
    wait = WebDriverWait(driver, 30)
    driver.get('http://172.16.100.1:4444')
    
    print("Navigation réussie")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    if 'driver' in locals():
        driver.quit()
