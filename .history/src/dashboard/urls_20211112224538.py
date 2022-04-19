from django.urls import path, include
import dashboard.views as views

urlpaterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
]