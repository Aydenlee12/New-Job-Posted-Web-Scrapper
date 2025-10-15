import requests
from job import Job

WEBHOOK_URL = "https://discord.com/api/webhooks/1427808959594500238/dUwGdZvW3enGsjZzMI4plGff7rdbfZnhvYYcufjFYXGTMld4zepZqza6_kdVc0HmkoE5"

def send_to_discord(job: Job):
    data = {
        "content": str(job)
    }
    requests.post(WEBHOOK_URL, json=data)
