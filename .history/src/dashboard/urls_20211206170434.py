from django.urls import path
import dashboard.views as views


urlpatterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
    path('emails/', views.EmailsView.as_view(), name="emails-dashboard"),
    path('users/', views.UsersView.as_view(), name="users-dashboard"),
    
    # service paths/urls
    path('services/', views.ServicesView.as_view(), name="services-dashboard"),
    path('services/add', views.add_service.as_view(), name="services-add"),
    path('services/delete/<int:id>', views.delete_service, name="services-delete"),
    path('services/edit/<int:id>', views.edit_service.as_view(), name="services-edit"), 
    
    # email
    <path:>   
]