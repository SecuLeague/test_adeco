from selenium import webdriver
from chromedriver_py import binary_path
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
driver.get('http://172.16.100.1:4444")
input("Press any key to exit.")
driver.quit()