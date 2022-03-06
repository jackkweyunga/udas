from django.urls import path
import dashboard.views as views
import users.views as user_views



urlpatterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
    
    # user view
    path('users/', views.UsersView.as_view(), name="users-dashboard"),
    path('users/<pk>/delete', views.UserDeleteView.as_view(), name="user-delete"),
    path("user/<int:id>/", views.user_view, name="user"),   
    
    
    # email view
    path('emails/', views.EmailsView.as_view(), name="emails-dashboard"),
    path('emails/', views.EmailsView.as_view(), name="emails"),
    path("email/<int:id>/", views.email_view.as_view(), name="email"),
    path("send_test_email/<int:email_id>/", user_views.send_test_email , name="send_test_email"),
    
    
    # service paths/urls
    path('services/', views.ServicesView.as_view(), name="services-dashboard"),
    path('services/add', views.add_service.as_view(), name="services-add"),
    path('services/delete/<int:id>', views.delete_service, name="services-delete"),
    path('services/edit/<int:id>', views.edit_service.as_view(), name="services-edit"), 
]