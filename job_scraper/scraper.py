from login import Setup
from delay import TimeDelay as td
from configparser import ConfigParser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()    # reads .env file  na dload all variables into environement

CONFIG = {
    "gmail_address": os.environ.get("GMAIL_ADDRESS"),
    "gmail_password": os.environ.get("GMAIL_APP_PASSWORD"),
    "target_email_address": os.environ.get("TARGET_EMAIL_ADDRESS")
}

setup = Setup()

# call driver object
driver = setup.set_driver()


class JobScrapper():

    def user_login(self, url, username, password):
        driver.get(url)
        # setup.load_cookies(driver)
        td.interval()

        driver.find_element(By.ID, username).send_keys(email)
        td.interval()
        driver.find_element(By.ID, password).send_keys(passwd)
        td.interval()
        driver.find_element(By.XPATH, "//button[@type='submit']").click()



        # if driver.find_elements(By.LINK_TEXT, 'Sign in'):
        #     driver.find_element(By.ID, username).send_keys(email)
        #     td.interval()
        #     driver.find_element(By.ID, password).send_keys(passwd)
        #     td.interval()
        #     driver.find_element(By.XPATH, "//button[@type='submit']").click()

        #     # Save cookies for future
        #     setup.save_cookies(driver)
        # else:
        #     print("Previous session loaded")
    
    def search_job(self, job_title):
        driver.find_element(By.XPATH, '//*[@id=":r2:"]').send_keys(job_title)
        td.interval()
        driver.get(f"https://www.linkedin.com/jobs/search-results/?keywords={job_title}")
        td.interval()

        # Include Remote jobs
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]/div/div/div/div/div/div/div[3]/div/div/label[contains(text(), "Remote")]').click()
        td.interval()

        # Select past week jobs
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]//label[contains(text(), "Date posted")]').click()
        td.interval()
        driver.find_element(By.XPATH, '//div/div/div[1]/div/div[2]/div/div[2]/p[contains(text(), "Past week")]').click()
        td.interval()
        driver.find_element(By.LINK_TEXT, "Show results").click()
        td.interval()

        # Select Experience Level
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]//label[contains(text(), "Experience level")]').click()
        td.interval()
        # Select experience level as Entry-level
        driver.find_element(By.XPATH, '//div/div/div[1]/div/div[1]/div/div/div[2]/p[contains(text(), "Entry-level")]').click()
        td.interval()
        # Show results of Entry-level jobs
        driver.find_element(By.LINK_TEXT, "Show results").click()
        td.interval()

        
    def scrapper(self):
        job_data = []
        
        for num in range(0, 10):
            job_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[1]/div[1]/div/div[1]/p/span[2]'
            company_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[1]/div[1]/div/div[2]/p'
            location_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[1]/div[1]/div/p'
            date_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[2]//span[1][contains(text(), "Posted")]'

            # try:
            #     job_name = job_title.find_element(By.XPATH, "./span[2]").text
            # except Exception:
            #     job_name = job_title.text

            job_name = driver.find_element(By.XPATH, job_path).text
            company = driver.find_element(By.XPATH, company_path).text
            job_location = driver.find_element(By.XPATH, location_path).text
            date_posted = driver.find_element(By.XPATH, date_path).text

            # print(f"Job {num+1}")
            # print("\t", job_name)
            # print("\t", company)
            # print("\t", job_location)
            # print("\t", date_posted)
            
            job_data.append([job_name, company, job_location, date_posted])

        return job_data
