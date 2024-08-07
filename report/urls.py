from django.urls import path

# from . import views
from .views import ReportTransactions, SummaryReportTransactions

urlpatterns = [
    # path('', views.index, name='index')
    path('report', ReportTransactions.as_view(), name='report-transactions'),
    path('summary-report', SummaryReportTransactions.as_view(), name='summary-report-transactions'),
]
