from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('report.urls')),
    path('api/', include('report.urls')),
    path('api/notification', include('notification.urls')),
]
