"""This script scrapes job offers from indeed.com"""
import csv
import sys

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
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")

offer = input("Enter the job you want to search for: ").strip()
country = input("Enter the country you want to search in: ").strip()
num_pages = int(input("Enter the number of pages you want to scrape: "))

job_data = []
# just for the loading animation
print("Loading:")
animation = "|/-\\"
for i in range(num_pages):
    sys.stdout.write("\r" + animation[i % len(animation)])
    sys.stdout.flush()
    page = scraper.get(
        f"https://ma.indeed.com/jobs?q={offer.replace(' ','+')}&l={country.replace(' ','+')}&sort=date&start={str(i*10)}",
        headers=headers,
    )

    def get_job_info():
        """This function gets the job information"""
        soup = BeautifulSoup(page.content, "lxml")
        # get the job offers
        job_offer = soup.find_all("div", {"class": "cardOutline"})
        for job in job_offer:
            job_title = job.find("h2", {"class": "jobTitle"}).text.strip()
            # get the company name
            job_company = job.find("div", {"class": "company_location"}).find(
                "span", {"class": "companyName"}
            )
            if job_company is None:
                job_company = "Not specified"
            else:
                job_company = job_company.text.strip()
            # get the job description
            job_description = job.find("div", {"class": "job-snippet"}).text.strip()
            # get the job salary
            job_salary = job.find("div", {"class": "salary-snippet-container"})
            if job_salary is None:
                job_salary = "Not specified"
            else:
                job_salary = job_salary.text.strip()
            # get the last update
            job_last_update = (
                job.find("span", {"class": "date"}).text.strip().replace("Posted", "")
            )
            job_link = "https://ma.indeed.com" + (
                job.find("a", {"class": "jcs-JobTitle"}).get("href")
            )
            # append the data to the list
            job_data.append(
                {
                    "Job title": job_title,
                    "Company": job_company,
                    "Description": job_description,
                    "Job salary": job_salary,
                    "Last update": job_last_update,
                    "Job link": job_link,
                }
            )

    get_job_info()
# save the data in a csv file
if len(job_data) == 0:
    print("No job found, try again")
else:
    keys = job_data[0].keys()
    with open("jobs.csv", "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, keys)
        writer.writeheader()
        writer.writerows(job_data)
        print("======file created successfully======")
