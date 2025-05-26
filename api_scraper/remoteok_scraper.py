import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from bs4 import BeautifulSoup
import re
import os
BASE_URL = 'https://remoteok.com/api'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
REQUEST_HEADER = {
    'User-Agent': USER_AGENT,
    'Accept-Language': 'en-US, en;q=0.5',
}

# Added clean_text function to strip HTML tags from description and normalize text, returning "N/A" for empty inputs.
def clean_text(text):
    """Remove HTML tags, extra whitespace, and normalize text."""
    if not text:
        return "N/A"
    soup = BeautifulSoup(text, "html.parser")
    clean = soup.get_text(separator=" ")
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean

# Added validate_salary function to convert salaries to integers, handling invalid or missing values by returning 0.
def validate_salary(salary):
    """Ensure salary is a valid number; return 0 if invalid."""
    try:
        return int(salary) if salary else 0
    except (ValueError, TypeError):
        return 0

def get_job_postings():
    """Fetch job postings from RemoteOK API."""
    try:
        res = requests.get(url=BASE_URL, headers=REQUEST_HEADER)
        res.raise_for_status()  # Raise an error for bad responses
        return res.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def output_jobs_to_xls(data):
    """Write cleaned job data to an Excel file."""
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs')
    
    # Define headers explicitly to ensure consistency
    headers = ['slug', 'id', 'epoch', 'date', 'company', 'company_logo', 'position','tags', 'logo', 'description', 'location', 'salary_min','salary_max','apply_url', 'url']


    for i in range(0, len(headers)):
        job_sheet.write(0,i,headers[i])

    for i, job in enumerate(data):
        # Clean and validate fields
        cleaned_job = {
            'slug': job.get('slug', 'N/A'),
            'id': job.get('id', 'N/A'),
            'epoch': job.get('epoch', 0),
            'date': job.get('date', 'N/A'),
            'company': job.get('company', 'N/A'),
            'company_logo': job.get('company_logo', 'N/A'),
            'position': job.get('position', 'N/A'),
            'tags': ', '.join(job.get('tags', [])) if isinstance(job.get('tags'), list) else 'N/A',
            'logo': job.get('logo', 'N/A'),
            'description': clean_text(job.get('description', '')),
            'location': job.get('location', 'N/A'),
            'salary_min': validate_salary(job.get('salary_min')),
            'salary_max': validate_salary(job.get('salary_max')),
            'apply_url': job.get('apply_url', 'N/A'),
            'url': job.get('url', 'N/A')
        }
        
# Modified loop to create a cleaned_job dictionary, applying clean_text to description, validate_salary to salaries, and handling missing fields with .get(). Tags are joined into a string for readability.
        for x, value in enumerate(cleaned_job.values()):
            job_sheet.write(i + 1, x, value)
    # Ensure the 'api_scraper' directory exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'api_scraper_output_xls')
    os.makedirs(output_dir, exist_ok=True)  # Create the folder if it doesn't exist
    output_path = os.path.join(output_dir, 'remote_jobs.xls')
    wb.save(output_path)
    print(f"Excel file saved to: {output_path}")

if __name__ == "__main__":
    json = get_job_postings()[1:]
    output_jobs_to_xls(json)