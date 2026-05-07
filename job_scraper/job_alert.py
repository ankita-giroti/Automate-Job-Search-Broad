import pandas as pd
import yaml
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()        # reads the .env file and loads all variables into environment

CONFIG = {
    'gmail_address': os.environ.get('GMAIL_ADDRESS'),
    'gmail_pass': os.environ.get('GMAIL_APP_PASSWORD'),
    'target_email': os.environ.get('TARGET_EMAIL_ADDRESS')
}

class EmailAlertSystem:
    
    def __init__(self):
        pass
    
    def access_data(self, file):
        job_data = pd.read_csv(file)
        
        job_list = []
        
        for i in range(0, len(job_data)):
            job_role = job_data['Job'].iloc[i]
            company = job_data['Company'].iloc[i]
            location = job_data['Location'].iloc[i]
            job_type = job_data['Type'].iloc[i]
            date_posted = job_data['Date Posted'].iloc[i]
            
            job = [job_role, company, location, job_type, date_posted]

            job_list.append(job)
        
        return job_list
    
    
    def email_alert(self, job_data):
        cards = ""
        
        for job in job_data:
            role, company, location, job_type, date_posted = map(str, job)
            
            card = f"""
            <div class="job-role">
                <h3 class="job-card">{role}</h3>

                <p><span class="label">Company:</span> {company}</p>
                <p><span class="label">Location:</span> {location}</p>
                <p><span class="label">Job Type:</span> {job_type}</p>
                <p><span class="label">Date Posted:</span> {date_posted}</p>
            </div>
            """
            
            cards += card
            
        with open("./static/email_card.html", "r", encoding="utf-8") as html:
            html_template = html.read()
            
        content = html_template.replace("{{ JOB_CARDS }}", cards)
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Top Job Alerts"
        message['To'] = CONFIG.get('target_email')
        message['From'] = CONFIG.get('gmail_address')
        
        msg = MIMEText(content, 'html')
        message.attach(msg)


        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(CONFIG.get('gmail_address'), CONFIG.get('gmail_pass'))
            smtp.sendmail(CONFIG.get('gmail_address'), CONFIG.get('target_email'), message.as_string())
        
        
sys = EmailAlertSystem()
job_data = sys.access_data("../job_csv_files/jobs_cleaned.csv")
# print(job_data)
sys.email_alert(job_data)
