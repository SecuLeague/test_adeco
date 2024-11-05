from selenium import webdriver
from chromedriver_py import binary_path
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
driver.get('https://172.16.0.90:443')
input("Press any key to exit.")
driver.quit()