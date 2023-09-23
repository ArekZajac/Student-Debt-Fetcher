import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

debt = ""

class Instance:

    def __init__(self):

        load_dotenv()
        
        global debt
        debt = self.GetDebt()
        
    
    def InitDriver(self):

        options = webdriver.ChromeOptions()
        if os.getenv("HEADLESS", 'False').lower() in ('true', '1', 't'):
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
        
        return driver
    
    def GetDebt(self):

        driver = self.InitDriver()

        driver.get("https://www.manage-student-loan-balance.service.gov.uk/ors/account-overview/secured/summary?locale=en")

        try: driver.find_element(By.XPATH, '//*[@id="accept-cookies"]').click()
        except: pass

        driver.find_element(By.XPATH, '//*[@id="userId"]').send_keys(os.getenv('USERNAME'))
        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(os.getenv('PASSWORD'))
        driver.find_element(By.XPATH, '//*[@id="action-primary-0"]').click()
        driver.find_element(By.XPATH, '//*[@id="secretAnswer"]').send_keys(os.getenv('SECRET'))
        driver.find_element(By.XPATH, '//*[@id="action-primary-0"]').click()

        debt = driver.find_element(By.XPATH, '//*[@id="balanceId_1"]').text
        driver.quit()
        return debt

if __name__ == "__main__":
    newInstance = Instance()
    print(debt)