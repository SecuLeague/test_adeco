from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Setup Chrome WebDriver with WebDriver Manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Navigate to the URL (fixed quotes)
    driver.get('http://172.16.100.1:4444')
    
    # Wait for user input
    input("Press any key to exit.")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    # Ensure the driver is closed properly
    if 'driver' in locals():
        driver.quit()
