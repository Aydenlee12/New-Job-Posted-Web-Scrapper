import requests
from job import Job

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

def send_to_discord(job: Job):
    data = {
        "content": str(job)
    }
    requests.post(WEBHOOK_URL, json=data)
