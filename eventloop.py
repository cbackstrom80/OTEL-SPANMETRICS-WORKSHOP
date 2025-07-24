import time
import requests

# === Config ===
url = "https://ingest.us1.signalfx.com/v2/event"
token = "dkylUMnNoi1m8YKq9awXNg"
headers = {
    "Content-Type": "application/json",
    "X-SF-Token": token
}

# Start time in milliseconds
base_timestamp = int(time.time() * 1000)

# === Send 300 events ===
for i in range(300):
    ts = base_timestamp + (i * 1000)  # 1-second increment

    body = f'''[
        {{
            "category": "USER_DEFINED",
            "eventType": "CB Spam Sold Event",
            "timestamp": {ts},
            "severity": "INFO",
            "dimensions": {{
                "environment": "production",
                "service": "API",
                "product": "SPAM"
            }},
            "properties": {{
                "sha1": "1234567890abc",
                "event_number": "{i + 1}",
                "injected_token": "{token}"
            }}
        }}
    ]'''

    response = requests.post(url, headers=headers, data=body)
    print(f"Event {i + 1} → Status {response.status_code}")
    if response.status_code >= 400:
        print("Error response:", response.text)
