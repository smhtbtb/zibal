import asyncio

from notification.notifications.abstract_notification import AbstractNotification


class EmailNotification(AbstractNotification):
    async def send_message(self, subject, message, recipient):
        await asyncio.sleep(3)
        print(f"Sending email {subject} to {recipient}: {message}")
