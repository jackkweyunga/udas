from django.urls import path
import dashboard.views as views
import smsbot.views as views



urlpatterns = [
    path('send-test-sms/', views.SendTestSmsView.as_view(), name="send-test-sms"),
]
    