from django.urls import path
import fakate.views as views



urlpatterns = [
    
    path('fakate/', views.AllFakateView.as_view(), name="fakate"),
    path('fakate/<int:id>', views.FakateView.as_view(), name="fakate-view"),

]