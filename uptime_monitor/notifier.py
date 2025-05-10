import requests
from typing import Optional
import logging


class TelegramNotifier:
    def __init__(self, token: Optional[str], chat_id: Optional[str], logger: Optional[logging.Logger] = None):
        self.token = token
        self.chat_id = chat_id
        self.logger = logger or logging.getLogger(__name__)

        if not self.is_configured():
            self.logger.warning("TelegramNotifier is not fully configured. Notifications will be skipped.")

    def is_configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send_message(self, message: str) -> None:
        if not self.is_configured():
            self.logger.warning("Attempted to send a notification, but TelegramNotifier is not configured.")
            return

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.error(f"Failed to send Telegram notification: {e}")
