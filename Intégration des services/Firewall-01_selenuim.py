from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

try:
    # Setup Chrome WebDriver with WebDriver Manager
    options = webdriver.ChromeOptions()
    # Specify the path to the Chrome binary if necessary
    # options.binary_location = "/path/to/chrome"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Navigate to the URL
    driver.get('http://172.16.100.1:4444')
    
    # Wait for user input
    input("Press any key to exit.")

except Exception as e:
    print(f"Error occurred: {str(e)}")

finally:
    # Ensure the driver is closed properly
    if 'driver' in locals():
        driver.quit()
