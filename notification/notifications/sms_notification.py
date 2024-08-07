import asyncio

from notification.notifications.abstract_notification import AbstractNotification


class SMSNotification(AbstractNotification):
    async def send_message(self, subject, message, recipient):
        await asyncio.sleep(2)
        print(f"Sending sms {subject} to {recipient}: {message}")
