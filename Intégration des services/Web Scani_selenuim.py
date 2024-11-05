from selenium import webdriver
from chromedriver_py import binary_path
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
driver.get('http://192.168.10.12:8080')
input("Press any key to exit.")
driver.quit()