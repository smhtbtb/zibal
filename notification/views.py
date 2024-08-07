import asyncio

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.notification_service import NotificationService


class SendNotification(APIView):
    def post(self, request):
        mediums = request.data['mediums']
        subject = request.data['subject']
        message = request.data['message']
        recipient = request.data['recipient']
        notification_service = NotificationService(mediums)
        # notif = notification_service.notify(subject, message, recipient)
        asyncio.run(notification_service.notify(subject, message, recipient))
        return Response({"status": "Notification(s) sent"}, status=status.HTTP_200_OK)
