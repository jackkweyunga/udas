from django.urls import path, include
import .views as 

urlpaterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
]