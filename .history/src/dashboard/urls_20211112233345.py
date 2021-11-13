from django.urls import path
import dashboard.views as views

urlpatterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
    path('emails/', views.IndexView.as_view(), name="dashboard"),
    path('users/', views.IndexView.as_view(), name="dashboard"),
    path('services/', views.IndexView.as_view(), name="dashboard"),
    
]