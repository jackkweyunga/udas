from django.urls import path, include
import views

urlpaterns = [
    path('', views.IndexView)
]