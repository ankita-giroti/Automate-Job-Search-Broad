from scraper import JobScrapper
from delay import TimeDelay as td
from csv_job import WriteJobs
from dotenv import load_dotenv
import os

if __name__=="__main__":

    load_dotenv()  # reads the .env file and loads all variables into environment

    CONFIG = {
        "target_url": os.environ.get("TARGET_URL1"),
        "website_user_id": os.environ.get("TARGET_URL_UID1"),
        "website_user_password": os.environ.get("TARGET_URL_PASSWORD1")
    }

    job = JobScrapper()

    job.user_login(CONFIG['target_url', CONFIG['website_user_id'], CONFIG['website_user_password'])
    td.interval()
    job.search_job("data analyst and data science")
    
    td.interval()
    
    job_data = job.scrapper()
    print("Scraping Done.")
    
    # td.interval()
    
    write_jobs = WriteJobs()
    write_jobs.write_to_csv(job_data)
    write_jobs.clean_job_data("./csv_data/jobs.csv")
