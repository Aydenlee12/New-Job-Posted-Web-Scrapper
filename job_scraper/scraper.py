"""
scraper.py - Indeed scraper using undetected_chromedriver (uc)
Installs:
    pip install undetected-chromedriver selenium requests
"""

from typing import List
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, os, re, warnings, ctypes
from job import Job
from discord_notifier import send_to_discord


# =========================
# 1️⃣ Helper Functions
# =========================
def build_driver() -> uc.Chrome:
    """Create an undetected-chromedriver instance that bypasses login prompts."""
    options = uc.ChromeOptions()
    # options.add_argument("--headless=new")  # optional
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Use a common desktop user-agent
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
    options.add_argument(f"--user-agent={ua}")

    driver = uc.Chrome(version_main=140, options=options)

    # Go to the base site first to set guest cookies
    driver.get("https://www.indeed.com")
    
    # Add a guest cookie (this helps skip login overlays)
    driver.add_cookie({
        "name": "CTK",
        "value": "guest",  # indicates guest mode
        "domain": ".indeed.com",
        "path": "/",
    })
    
    driver.set_page_load_timeout(60)
    return driver

# =========================
# 2️⃣ Main Scraper
# =========================
def scrape_jobs(max_pages: int = 3, location_encoded: str = "Minneapolis%2C+MN") -> List[Job]:
    """
    Scrape Indeed for recent software engineer jobs.
    Sends all found jobs directly to Discord.
    """
    base_url = f"https://www.indeed.com/jobs?q=software+engineer&l={location_encoded}&fromage=7"
    driver = build_driver()
    collected = []

    print("🌐 undetected-chromedriver started — scraping Indeed...")

    try:
        for page in range(max_pages):
            start = page * 10
            url = f"{base_url}&start={start}"
            print(f"\n📄 Loading page {page + 1}: {url}")
            driver.get(url)

            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.job_seen_beacon"))
                )
            except Exception:
                print("⚠️ Timeout — no jobs loaded.")
                continue

            job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job_seen_beacon")
            print(f"🔍 Found {len(job_cards)} job cards on page {page + 1}.")

            for card in job_cards:
                try:
                    title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text.strip()
                    company = card.find_element(By.CSS_SELECTOR, "span.companyName").text.strip() if card.find_elements(By.CSS_SELECTOR, "span.companyName") else "Unknown"
                    location = card.find_element(By.CSS_SELECTOR, "div.companyLocation").text.strip() if card.find_elements(By.CSS_SELECTOR, "div.companyLocation") else "Unknown"
                    link = card.find_element(By.CSS_SELECTOR, "h2.jobTitle a").get_attribute("href")
                    try:
                        posted = card.find_element(By.CSS_SELECTOR, "span.date").text.strip()
                    except:
                        posted = "Recently"

                    print(f"⏰ {title} — {posted}")

                    # ✅ Send all jobs to Discord (filter removed for testing)
                    job = Job(title, company, location, link)
                    collected.append(job)
                    send_to_discord(job)
                    time.sleep(0.5)  # small pause to avoid hitting webhook rate limit

                except Exception as e:
                    continue

            time.sleep(2)

    finally:
        driver.quit()
        print(f"\n🎯 Done. Sent {len(collected)} jobs to Discord.")

        # suppress "WinError 6" cleanup warning
        try:
            warnings.filterwarnings("ignore", category=ResourceWarning)
            ctypes.windll.kernel32.SetConsoleCtrlHandler(None, 0)
        except Exception:
            pass

    return collected


# =========================
# 3️⃣ Script Entry Point
# =========================
if __name__ == "__main__":
    print("🚀 Starting scraper...")
    jobs = scrape_jobs(max_pages=3, location_encoded="Minneapolis%2C+MN")
    print(f"\n✅ Done! Found {len(jobs)} jobs total.")
    for j in jobs:
        print("\n---")
        print(j)
