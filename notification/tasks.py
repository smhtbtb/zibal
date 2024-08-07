# from celery import shared_task
# from .notification_service import NotificationService
#
#
# @shared_task
# def send_notification(subject, medium, message, recipient):
#     service = NotificationService(medium)
#     service.notify(subject, message, recipient)

from celery import shared_task

from notification.notifications.notification_factory import NotificationFactory


# from .notification_service import NotificationService


@shared_task(bind=True, max_retries=3)
def send_notification_task(self, medium, subject, message, recipient):
    # service = NotificationService(medium)

    # strategy.send_message(subject, message, recipient)

    strategy = NotificationFactory.get_strategy(medium)
    try:
        strategy.send_message(subject, message, recipient)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
