import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

class DebtFetcher:
    def __init__(self):
        try:
            load_dotenv()
            self.username = os.getenv('USERNAME')
            self.password = os.getenv('PASSWORD')
            self.secret = os.getenv('SECRET')
        except: pass

    def init_driver(self):
        options = webdriver.ChromeOptions()
        if os.getenv("HEADLESS", 'False').lower() in ('true', '1', 't'):
            options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)
    
    def get_debt_info(self, *args):
        try:
            self.username = args[0]
            self.password = args[1]
            self.secret = args[2]
        except: pass 

        driver = self.init_driver()
        url = "https://www.manage-student-loan-balance.service.gov.uk/ors/account-overview/secured/summary?locale=en"
        driver.get(url)
        self.accept_cookies(driver)

        try:
            self.login(driver)
        except: print("Incorrect details provided")

        debt = float(self.extract_debt(driver)[1:].replace(",",""))
        rate = float(self.extact_rate(driver)[:-1])
        asof = self.extract_asof(driver).replace("as of ","")
        driver.quit()
        return debt, rate, asof
    
    def accept_cookies(self, driver):
        try:
            driver.find_element(By.XPATH, '//*[@id="accept-cookies"]').click()
        except:
            pass  # Consider logging the exception
    
    def login(self, driver):
        driver.find_element(By.XPATH, '//*[@id="userId"]').send_keys(self.username)
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.password)
        driver.find_element(By.XPATH, '//*[@id="action-primary-0"]').click()
        driver.find_element(By.XPATH, '//*[@id="secretAnswer"]').send_keys(self.secret)
        driver.find_element(By.XPATH, '//*[@id="action-primary-0"]').click()
    
    def extract_debt(self, driver):
        return driver.find_element(By.XPATH, '//*[@id="balanceId_1"]').text.strip()
    
    def extact_rate(self, driver):
        return driver.find_element(By.XPATH, '//*[@id="interestAsOfDateId-1"]').text
    
    def extract_asof(self, driver):
        return driver.find_element(By.XPATH, '//*[@id="asOfBalanceDateId-1"]').text 


if __name__ == "__main__":
    print("Fetching debt info...")
    debt_fetcher = DebtFetcher()
    debt, rate, asof = debt_fetcher.get_debt_info()
    print(f"Current debt is £{debt},\nat a rate of {rate}%,\nas of {asof}.")
