from django.urls import path
import fakate.views as views



urlpatterns = [
    
    path('fakate/', views.FakateView.as_view(), name="fakate"),
    path('fakate/intents', views.FakateIntents.as_view(), name="fakate-intents"),
    path("fakate/intent-labels", views.FakateIntentLabels.as_view(), name="fakate-intent-labels"),

]