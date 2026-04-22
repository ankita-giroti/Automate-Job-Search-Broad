from scraper import JobScrapper
from delay import TimeDelay as td
from csv_job import WriteJobs

if __name__=="__main__":

    job = JobScrapper()

    job.user_login("https://www.linkedin.com/jobs", "session_key", "session_password")
    td.interval()
    job.search_job("data analyst and data science")
    
    td.interval()
    
    job_data = job.scrapper()
    print("Scraping Done.")
    
    # td.interval()
    
    write_jobs = WriteJobs()
    write_jobs.write_to_csv(job_data)
    write_jobs.clean_job_data("./csv_data/linkedin_jobs.csv")