from login import Setup
from delay import TimeDelay as td
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    'gmail_address': os.environ.get('GMAIL_ADDRESS'),
    'gmail_passwd': os.environ.get('GMAIL_APP_PASSWORD'),
    'website_pass': os.environ.get('WEB_APP1_PASSWORD'),
    'website_url': os.environ.get('TARGET_URL1')
}

setup = Setup()

# call driver object
driver = setup.set_driver()


class JobScrapper():

    def user_login(self, url, username, password):
        driver.get(url)

        WebDriverWait(driver, 50).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        setup.load_cookies(driver)
        
        try:    
            if driver.find_elements(By.LINK_TEXT, 'Sign in'):
                username = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, username)))
                username.send_keys(CONFIG.get('gmail_address'))
                password = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, password)))
                password.send_keys(CONFIG.get('website_pass'))

                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()

                # # Save cookies for future
                # setup.save_cookies(driver)
            else:
                print("Previous session loaded")
        except TimeoutException:
            print("Elements not found within 30 seconds - page may not have loaded correctly")
            driver.save_screenshot("debug_screenshot.png")
    
    def search_job(self, job_title):
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Describe the job you want"]'))).send_keys(job_title)
        driver.get(f"{CONFIG.get('website_url')}/search-results/?keywords={job_title}")

        # Include Remote jobs
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]//label[contains(text(), "Remote")]'))).click()

        # Select past week jobs
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]//label[contains(text(), "Date posted")]'))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//p[contains(text(), "Past week")]'))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Show results"))).click()

        # Select Experience Level
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[2]//label[contains(text(), "Experience level")]'))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//div/div/div[1]/div/div[1]/div/div/div[2]/p[contains(text(), "Entry-level")]'))).click()
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, "Show results"))).click()

        
    def scrapper(self):
        job_data = []
        
        for num in range(0, 10):
            job_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[1]/div[1]/div/div[1]/p/span[2]'
            company_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[1]/div[1]/div/div[2]/p'
            location_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[1]/div[1]/div/p'
            date_path = f'//*[@id="workspace"]/div/div/div[1]/div/div/div[{num+1}]/div/div/div/div/div/div/div[2]//span[1][contains(text(), "Posted")]'

            # Job Title
            job_name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, job_path))).text

            # Company
            company = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, company_path))).text

            # Location
            job_location = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, location_path))).text

            # Date posted
            date_posted = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, date_path))).text

            # print(f"Job {num+1}")
            # print("\t", job_name)
            # print("\t", company)
            # print("\t", job_location)
            # print("\t", date_posted)
            
            job_data.append([job_name, company, job_location, date_posted])

        return job_data
