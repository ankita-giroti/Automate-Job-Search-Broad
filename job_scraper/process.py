from scraper import JobScrapper
from delay import TimeDelay as td
from csv_job import WriteJobs
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG = {
    "target_website": os.environ.get('TARGET_URL1'),
    "session_key": os.environ.get('TARGET_URL_UID1'),
    "session_password": os.environ.get('TARGET_URL_PASSWORD1'),
}

if __name__=="__main__":

    job = JobScrapper()

    job.user_login(CONFIG.get('target_website'), CONFIG.get("session_key"), CONFIG.get("session_password"))
    td.interval()
    job.search_job("data analyst and data science")
    
    td.interval()
    
    job_data = job.scrapper()
    print("Scraping Done.")
    
    # td.interval()
    
    write_jobs = WriteJobs()
    write_jobs.write_to_csv(job_data)
    write_jobs.clean_job_data("job_csv_files/jobs.csv")
