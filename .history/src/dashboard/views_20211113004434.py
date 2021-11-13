from django.shortcuts import render
from django.views import View 
from django.views.generic import ListView
from users.models import User, DynamicEmailConfiguration

# Create your views here.

class IndexView(View):
    
    """ Index View """  

    
    def get(self, request):
        
        context = {
        
        }
        return render(request, "dashboard/index.html", context=context)


class EmailsView(View):
    
    def get(self, request):
        all = DynamicEmailConfiguration.objects.all()
        context = {
            
            "emails":all,
            "count":all.cou
            
        }
        
        return render(request, 'dashboard/emails.html', context)
    
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