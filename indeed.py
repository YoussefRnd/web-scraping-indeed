import csv

import cloudscraper
import requests
from bs4 import BeautifulSoup

headers = {
    "x-api-key": "cf82404402779d28ecfd584bb1295496",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Accept": "text/html",
    "Referer": "https://www.example.com",
    "Connection": "keep-alive",
    "Accept-Encoding": "gzip, deflate",
}
# jog = input("Enter the job you want to search for: ")
# country = input("Enter the country you want to search in: ")
scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
page = scraper.get(
    f"https://ma.indeed.com/jobs?q=python&l=Tanger&vjk=67d06dd02bdaf629",
    headers=headers,
)


def get_job_info():
    src = page.content
    soup = BeautifulSoup(src, "html.parser")
    job_data = []
    job_offer = soup.find_all("div", {"class": "cardOutline"})
    for job in job_offer:
        job_title = job.find("h2", {"class": "jobTitle"}).text.strip()
        job_company = job.find("div", {"class": "company_location"}).find(
            "span", {"class": "companyName"}
        )
        if job_company is None:
            job_company = "Company is not specified"
        else:
            job_company = job_company.text.strip()
        print(job_company)


get_job_info()
