from django.shortcuts import render
from django.views import View 
from django.views.generic import ListView
from users.models import User

# Create your views here.
class IndexView(View):
    """ Index View """  
    def get(self, requesst):
        pass
    
    
class UserListView(ListView):
    """Users List Views"""
    queryset = User
    template_name
    
        