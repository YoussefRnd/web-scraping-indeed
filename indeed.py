"""This script scrapes job offers from indeed.com"""
import csv

import cloudscraper
from bs4 import BeautifulSoup

# headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "text/html",
    "Referer": "https://www.example.com",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
}
offer = input("Enter the job you want to search for: ").strip()
country = input("Enter the country you want to search in: ").strip()
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
page = scraper.get(
    f"https://ma.indeed.com/jobs?q={offer.replace(' ','+')}&l={country.replace(' ','+')}",
    headers=headers,
)


print("======please wait======")
job_data = []


def get_job_info():
    """This function gets the job information"""
    soup = BeautifulSoup(page.content, "lxml")

    job_offer = soup.find_all("div", {"class": "cardOutline"})
    for job in job_offer:
        job_title = job.find("h2", {"class": "jobTitle"}).text.strip()

        job_company = job.find("div", {"class": "company_location"}).find(
            "span", {"class": "companyName"}
        )
        if job_company is None:
            job_company = "Not specified"
        else:
            job_company = job_company.text.strip()
        job_description = job.find("div", {"class": "job-snippet"}).text.strip()

        job_salary = job.find("div", {"class": "salary-snippet-container"})
        if job_salary is None:
            job_salary = "Not specified"
        else:
            job_salary = job_salary.text.strip()

        job_last_update = job.find("span", {"class": "date"}).text.strip().replace("Posted", "")

        job_data.append(
            {
                "Job title": job_title,
                "Company": job_company,
                "Description": job_description,
                "Job salary": job_salary,
                "Last update": job_last_update,
            }
        )


get_job_info()
# save the data in a csv file
keys = job_data[0].keys()
with open("jobs.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, keys)
    writer.writeheader()
    writer.writerows(job_data)
    print("======file created successfully======")
