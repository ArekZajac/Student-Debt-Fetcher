import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

class DebtFetcher:
    def __init__(self):
        load_dotenv()

    def init_driver(self):
        options = webdriver.ChromeOptions()
        if os.getenv("HEADLESS", 'False').lower() in ('true', '1', 't'):
            options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)
    
    def get_debt(self):
        driver = self.init_driver()
        url = "https://www.manage-student-loan-balance.service.gov.uk/ors/account-overview/secured/summary?locale=en"
        driver.get(url)
        self.accept_cookies(driver)
        self.login(driver)
        debt = self.extract_debt(driver)
        driver.quit()
        return debt
    
    def accept_cookies(self, driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="accept-cookies"]').click()
        except:
            pass  # Consider logging the exception
    
    def login(self, driver):
        driver.find_element(By.XPATH, '//*[@id="userId"]').send_keys(os.getenv('USERNAME'))
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.XPATH, '//*[@id="action-primary-0"]').click()
        driver.find_element(By.XPATH, '//*[@id="secretAnswer"]').send_keys(os.getenv('SECRET'))
        driver.find_element(By.XPATH, '//*[@id="action-primary-0"]').click()
    
    def extract_debt(self, driver):
        return driver.find_element(By.XPATH, '//*[@id="balanceId_1"]').text

if __name__ == "__main__":
    debt_fetcher = DebtFetcher()
    print(debt_fetcher.get_debt()) 
