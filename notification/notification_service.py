import asyncio
from datetime import datetime

from mongo_conn import get_db
from notification.notifications.notification_factory import NotificationFactory
# from notification.tasks import send_notification_task


class NotificationService:
    def __init__(self, mediums):
        # self.strategy = NotificationFactory.get_strategy(medium)
        self.strategies = [NotificationFactory.get_strategy(medium) for medium in mediums]

    # def notify(self, subject, message, recipient):
    #     try:
    #         self.strategy.send_message(subject, message, recipient)
    #         self.log_message(subject, message, recipient, self.strategy.__class__.__name__, 'success')
    #     except Exception as e:
    #         self.log_message(subject, message, recipient, self.strategy.__class__.__name__, 'failed')
    #         raise e

    async def notify(self, subject, message, recipient):
        tasks = [self._send_message(strategy, subject, message, recipient) for strategy in self.strategies]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                print(f"Error: {result}")

    async def _send_message(self, strategy, subject, message, recipient):
        try:
            await strategy.send_message(subject, message, recipient)
            self.log_message(subject, message, recipient, strategy.__class__.__name__, 'success')
        except Exception as e:
            self.log_message(subject, message, recipient, strategy.__class__.__name__, 'failed')
            raise e

    # def notify(self, subject, message, recipient):
    #     send_notification_task.delay(self.medium, subject, message, recipient)

    @staticmethod
    def log_message(subject, message, recipient, medium, status):
        db = get_db()
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        db.notification_log.insert_one({
            "subject": subject,
            "message": message,
            "recipient": recipient,
            "medium": medium,
            "status": status,
            "created_at": today,
        })
