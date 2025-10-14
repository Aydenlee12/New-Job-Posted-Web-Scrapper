from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from job import Job
from typing import List

def scrape_jobs() -> List[Job]:
    jobs = []
    url = "https://example.com/jobs"  # Replace with target site

    # Configure ChromeDriver
    service = Service('chromedriver')  # path to chromedriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # run without opening browser
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)
    
    # Find job listings
    listings = driver.find_elements(By.CLASS_NAME, "job-listing")  # adjust selector
    for el in listings:
        title = el.find_element(By.CLASS_NAME, "job-title").text
        company = el.find_element(By.CLASS_NAME, "company").text
        location = el.find_element(By.CLASS_NAME, "location").text
        link = el.find_element(By.TAG_NAME, "a").get_attribute("href")
        jobs.append(Job(title, company, location, link))
    
    driver.quit()
    return jobs
