import os
import requests
from dotenv import load_dotenv

class Telegram:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.id = os.getenv("CHAT_ID")
        if not self.token or not self.id:
            raise ValueError("Telegram token or chat ID is not set")

    def send_message(self, message: str) -> None:
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.id, "text": message}
        response = requests.post(url, json=payload)
        response.raise_for_status()


