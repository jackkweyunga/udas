from django.urls import path
import dashboard.views as views
import emails.views as email_views



urlpatterns = [
    path('', views.IndexView.as_view(), name="dashboard"),
    
    # user view
    path('users/', views.UsersView.as_view(), name="users-dashboard"),
    path('users/<pk>/delete', views.UserDeleteView.as_view(), name="user-delete"),
    path("user/<int:id>/", views.user_view, name="user"),   
    
    
    # email view
    path('emails/', views.EmailsView.as_view(), name="emails-dashboard"),
    path('emails/', views.EmailsView.as_view(), name="emails"),
    path('emails/<pk>/delete', views.EmailConfigurationDeleteView.as_view(), name="email-delete"),
    path("email/<int:id>/", views.email_view.as_view(), name="email"),
    path("send_test_email/<int:email_id>/", email_views.send_test_email , name="send_test_email"),
    
    # smsbot
    path('smsbots/', views.SmsBotsView.as_view(), name="smsbots"),
    path('smsbots/<pk>/delete', views.SmsBotDeleteView.as_view(), name="smsbot-delete"),
    path("smsbot/<int:id>/", views.SmsBotView.as_view(), name="smsbot"),


    # service paths/urls
    path('services/', views.ServicesView.as_view(), name="services-dashboard"),
    path('services/add', views.add_service.as_view(), name="services-add"),
    path('services/delete/<int:id>', views.delete_service, name="services-delete"),
    path('services/edit/<int:id>', views.edit_service.as_view(), name="services-edit"), 
]