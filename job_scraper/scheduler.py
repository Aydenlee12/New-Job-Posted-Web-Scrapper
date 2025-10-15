import schedule
import time
from scraper import scrape_jobs
from discord import send_to_discord

def job_task():
    print("Running LinkedIn scraper...")
    jobs = scrape_jobs()
    for job in jobs:
        send_to_discord(job)
    print(f"Sent {len(jobs)} tech jobs to Discord.")

# Run every 5 minutes
schedule.every(5).minutes.do(job_task)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(30)  # check schedule twice per minute
