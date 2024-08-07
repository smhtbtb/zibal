import asyncio

from mongo_conn import get_db
from notification.notification_service import NotificationService
from report.make_transaction_output import making_output

db = get_db()
merchant_ids = list(db.transaction.find({}, {"_id": 0, "merchantId": 1}))
merchant_ids = list(set([i["merchantId"] for i in merchant_ids]))

for merchant_id in merchant_ids:
    for type_ in ["amount", "count"]:
        this_result = making_output("daily", type_, merchant_id)
        mediums = ["email", "sms"]
        notification_service = NotificationService(mediums)
        subject = "Daily Report"
        message = this_result
        recipient = "user@example.com"
        asyncio.run(notification_service.notify(subject, message, recipient))


# DESIRED CRON JOB:
# 0 0 * * * /usr/bin/python /path/to/zibal/job_notifier.py
