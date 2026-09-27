import requests

# Your unique ntfy topic URL
url = "https://ntfy.sh/farmvibes_stemlink_1909"
url2 = "https://ntfy.sh/weather_i"

def send_notification(message):
    """Send a notification to the ntfy.sh service."""
    response = requests.post(
        url2,
        data=message.encode("utf-8"),
        headers={"Title":"@nipuna_gomes - Uria application advice "},
        timeout=10
    )

    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.status_code}")

send_notification(
    "No , It looks like it might rain in Gampaha tomorrow."
    "Do not to apply fertilizer for the field! I've sent this advice to your mobile"
)