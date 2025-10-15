import requests
# discord_notifier.py
import requests

WEBHOOK_URL = "https://discord.com/api/webhooks/1427809340752007248/S7tORtU3b-e10FDlsTCQWav_UHhcNjIyV6YJxnMuUZ_oKI2MIZLUaqSVUN56a2kARF7g"  # replace this with your own

def send_to_discord(job):
    """Send a job posting message to a Discord webhook."""
    data = {
        "content": f"**{job.title}** at {job.company}\n📍 {job.location}\n🔗 {job.link}"
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print(f"✅ Sent to Discord: {job.title}")
        else:
            print(f"⚠️ Discord returned {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Failed to send Discord message: {e}")
