from django.shortcuts import render
from django.views import View 
from django.views.generic import ListView
from users.models import User

# Create your views here.

class IndexView(View):
    
    """ Index View """  

    
    def get(self, request):
        
        context = {
        
        }
        return render(request, "dashboard/index.html", context=context)


class EmailsView(View):
    
    def get(self, request):
        
        context = {
            
        }
        
        return render(request, 'dashboard/emails.html')
    
class UsersView(View):
    
    def get(self, request):
        
        context = {
            
        }
        
        return render(request, 'dashboard/users.html')
    
class ServicesView(View):
    
    def get(self, request):
        
        context = {
            
        }
        
        return render(request, 'dashboard/services.html')