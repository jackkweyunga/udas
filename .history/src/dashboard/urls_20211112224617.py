from django.urls import path
import dashboard.views as views

url_paterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
]