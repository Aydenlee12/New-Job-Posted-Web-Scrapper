import schedule
import time
from scraper import scrape_jobs
from discord import send_to_discord

def job_task():
    print("Running scraper...")
    jobs = scrape_jobs()
    for job in jobs:
        send_to_discord(job)
    print(f"Sent {len(jobs)} jobs to Discord.")

# Run every hour
schedule.every(1).hours.do(job_task)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
