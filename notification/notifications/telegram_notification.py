import asyncio

from notification.notifications.abstract_notification import AbstractNotification


class TelegramNotification(AbstractNotification):
    async def send_message(self, subject, message, recipient):
        await asyncio.sleep(4)
        print(f"Sending telegram message {subject} to {recipient}: {message}")
