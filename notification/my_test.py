import asyncio
from notification.notification_service import NotificationService

# service = NotificationService('email')
subject = 'Daily Transaction Report'
message = 'Your daily transaction report is ready.'
recipient = 'user@example.com'
# # mediums = ['email', 'sms', 'push', 'telegram']
#
# print(service.notify(subject, message, recipient))


mediums = ['email', 'sms', 'telegram']
notification_service = NotificationService(mediums)


async def main():
    await notification_service.notify(subject, message, recipient)


asyncio.run(main())
