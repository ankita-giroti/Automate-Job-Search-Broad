import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from configparser import ConfigParser
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

constants = yaml.full_load(open('job_scraper/files/constants.yml'))
CHROME_DRIVER_ARGUMENTS = constants["constants"]["CHROME_DRIVER_ARGUMENTS"]

class Setup():
    def __init__(self):
        pass

    def set_driver(self):
        options = Options()
        for arg in CHROME_DRIVER_ARGUMENTS:
            options.add_argument(arg)

        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        driver.implicitly_wait(20)

        return driver

    # # Save cookies to JSON file
    # def save_cookies(self, driver):
    #     cookies = driver.get_cookies()
        
    #     with open('./files/cookies.json', 'w') as file:
    #         json.dump(cookies, file)
    #     print("New Cookies saved successfully")


    # Use cookies data for login
    def load_cookies(self, driver):
        if 'cookies.json' in os.listdir("./files"):
            cookies = os.environ.get('WEBSITE_DATA)

            for cookie in cookies:
                driver.add_cookie(cookie)
        else:
            print('No cookies file found')

        driver.refresh()
