from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from job import Job
from typing import List
import time

# Keywords to filter tech jobs
TECH_KEYWORDS = ["security", "software engineer", "developer", "IT", "technology"]

def is_tech_job(title: str) -> bool:
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in TECH_KEYWORDS)

def scrape_jobs() -> List[Job]:
    jobs = []

    # LinkedIn jobs URL (example: Software & IT jobs)
    url = "https://www.linkedin.com/jobs/search/?keywords=software%20engineer&location=United%20States"

    # Setup Selenium Chrome driver
    service = Service('chromedriver')  # path to your chromedriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)  # wait for page to load

    job_cards = driver.find_elements(By.CLASS_NAME, "base-card")  # LinkedIn job cards

    for card in job_cards:
        try:
            title = card.find_element(By.CLASS_NAME, "base-search-card__title").text
            company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text
            location = card.find_element(By.CLASS_NAME, "job-search-card__location").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

            if is_tech_job(title):
                jobs.append(Job(title, company, location, link))
        except Exception as e:
            continue  # skip any job card that fails

    driver.quit()
    return jobs
