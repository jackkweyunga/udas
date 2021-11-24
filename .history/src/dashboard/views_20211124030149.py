from django.shortcuts import render, redirect
from django.views import View 
from django.views.generic import ListView
from users.models import User, DynamicEmailConfiguration
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
# Create your views here.

class IndexView(LoginRequiredMixin, View):
    
    """ Index View """  

    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        
        context = {
        
        }
        return render(request, "dashboard/index.html", context=context)


class EmailsView(View):
    
    def get(self, request):
        all = DynamicEmailConfiguration.objects.all()
        context = {
            
            "emails":all,
            "count":all.count()
            
        }
        
        return render(request, 'dashboard/emails.html', context)
    
class UsersView(View):
    
    def get(self, request):
        
        all = User.objects.all()
        context = {
            
            "users":all,
            "count":all.count()
            
        }
        
        return render(request, 'dashboard/users.html', context)
    
class ServicesView(View):
    
    def get(self, request):
        
        context = {
            
        }
        
        return render(request, 'dashboard/services.html')
    
    

def login_view(request):
    if request.POST:
        
        form = LoginForm(data=request.POST)
        if form.is_valid():
            
            # check if creds are true
            data = form.cleaned_data
            user = authenticate(username=data["username"], password=data["password"])
            if user is not None:
                user = User.objects.filter(username=data["username"]).first()
                print("user")
                login(request, user=user)
                context = {"user":user}
                return redirect('dashboard')
            else:
                return redirect('login')  
        else:
            messages()
    else:
        context = {

        }
        return render(request, 'login_view.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')