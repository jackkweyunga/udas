from django.urls import path, include
import views

urlpaterns = [
    path('', views.IndexView, name="dashboard"),
    path('', views.UserViews.as_view({
        'get':
    }))
]