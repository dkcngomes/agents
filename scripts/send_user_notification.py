import requests
from langchain.tools import tool

url = "https://ntfy.sh/weather_i"

@tool
def send_notification(message: str) -> str:
    """Send a mobile notification message to the user. You MUST call this tool
    whenever the user asks to send a notification, notify them, or push an
    update to their phone.

    Args:
        message: The full text body to deliver to the user's phone.
    """

    print("<<<<< TOOL CALL send_notification >>>>>>>>")

    response = requests.post(
        url,
        data=message.encode("utf-8"),
        headers={"Title":"@nipuna_gomes - Apply fertilizer Weather update "},
    )

    if response.status_code == 200:
        print("Notification sent successfully!")
        return "Notification sent successfully!"
    else:
        print(f"Failed to send notification: {response.status_code}")
        return f"Failed to send notification: {response.status_code}"

