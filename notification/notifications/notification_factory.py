from notification.notifications.email_notification import EmailNotification
from notification.notifications.sms_notification import SMSNotification
from notification.notifications.telegram_notification import TelegramNotification


class NotificationFactory:
    @staticmethod
    def get_strategy(medium):
        if medium.lower() == 'email':
            return EmailNotification()
        elif medium.lower() == 'sms':
            return SMSNotification()
        elif medium.lower() == 'telegram':
            return TelegramNotification()
        else:
            raise ValueError("Invalid medium type")
