import csv
import pandas as pd

class WriteJobs():
    def write_to_csv(self, job_data):
        with open('./csv_data/linkedin_jobs.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Job", "Company", "Location", "Date Posted"])
            writer.writerows(job_data)


    def clean_job_data(self, file):
        job_data = pd.read_csv(file)

        split_locations = job_data["Location"].str.split("(", expand=True)
        split_locations.columns = ['job_location', 'type']
        split_locations['type'] = split_locations['type'].str.replace(')','')
        
        job_location = split_locations['job_location']
        job_type = split_locations['type']
        
        job_data['Location'] = job_location
        job_data['Type'] = job_type
        
        # Date posted
        date = job_data['Date Posted']
        # print(type(date))
        
        for d in date:
            clean_date = d.split(',')[2]
            clean_date = d.replace(clean_date, '').replace(',', '')
            clean_date = clean_date.replace("Posted on ", "")
            
        job_data['Date Posted'] = clean_date
        
        # Remove leading and trailing spaces
        job_data['Job'] = job_data['Job'].str.strip()
        job_data['Company'] = job_data['Company'].str.strip()
        job_data['Location'] = job_data['Location'].str.strip()
        job_data['Date Posted'] = job_data['Date Posted'].str.strip()
        job_data['Type'] = job_data['Type'].str.strip()
        
        job_data.to_csv('./csv_data/linkedin_jobs_cleaned.csv', index=False)
        
        print(job_data)