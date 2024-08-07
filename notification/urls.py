from django.urls import path
from .views import SendNotification

urlpatterns = [
    path('', SendNotification.as_view(), name='send-notification'),
]
