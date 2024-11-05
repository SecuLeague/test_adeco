from chromedriver_py import binary_path
svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)
driver.get('https://www.seculeague.link')
input("Press any key to exit.")
driver.quit