import requests

# Replace 'mytopic' with your unique, secret ntfy topic name
# (e.g., https://ntfy.sh/my-super-secret-backup-topic-9921)
url = "https://ntfy.sh/weather_i"


def send_notification(message: str):
    """Send a notification to the ntfy.sh service."""
    response = requests.post(
        url,
        data=message.encode("utf-8"),
    )

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.status_code}")

