import requests
from job import Job

WEBHOOK_URL = "https://discord.com/api/webhooks/1427808959594500238/dUwGdZvW3enGsjZzMI4plGff7rdbfZnhvYYcufjFYXGTMld4zepZqza6_kdVc0HmkoE5"
WEBHOOK_URL = "https://discord.com/api/webhooks/1427809223252639805/lofOvltzPFMK8ZplWJWaEWESU9uV9QBgQASKM3ppqIr2THi5S1a6-HtYn2AlBKxjUwzu"
WEBHOOK_URL = "https://discord.com/api/webhooks/1427809340752007248/S7tORtU3b-e10FDlsTCQWav_UHhcNjIyV6YJxnMuUZ_oKI2MIZLUaqSVUN56a2kARF7g"


def send_to_discord(job: Job):
    data = {
        "content": str(job)
    }
    requests.post(WEBHOOK_URL, json=data)
