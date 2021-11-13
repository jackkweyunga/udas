from django.urls import path
import dashboard.views as views

urlpaterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
]