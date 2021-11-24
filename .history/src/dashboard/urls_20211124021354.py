from django.urls import path
import dashboard.views as views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_requiredviews.IndexView.as_view(), name="dashboard"),
    path('emails/', views.EmailsView.as_view(), name="emails-dashboard"),
    path('users/', views.UsersView.as_view(), name="users-dashboard"),
    path('services/', views.ServicesView.as_view(), name="services-dashboard"),
    
]