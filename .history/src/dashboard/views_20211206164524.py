from django.shortcuts import render, redirect
from django.views import View 
from django.views.generic import ListView
from users.models import User, DynamicEmailConfiguration, Service, ServicePackage, ServiceUser, ServiceUserSubscription
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
            "services":Service.objects.all(),
            "user":request.user,
            "n_users":User.objects.all().count(),
            "n_emails":DynamicEmailConfiguration.objects.all().count(),
            
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
        all = Service.objects.all()
        context = {
            "services":all,
            "count": all.count()
        }
        
        return render(request, 'dashboard/services.html', context)


class add_service(View):
    # pass
    def post(self, request):
        
        id = request.POST.get("id", None)
        
        if id is not None:
            if Service.objects.filter(service_id=id).first():
                messages.error(request, "service exists")
                return redirect("services-dashboard")
            
                
            new = Service(service_id=id)
            new.save()
            messages.success(request, "service added")
            return redirect("services-dashboard")
        
        messages.error(request, "failed to add service")
        return redirect("services-dashboard")

class edit_service(View):
    # pass
    def post(self, request, id):
        new = Service.objects.filter(id=id).first()
        
        if Service.objects.filter(service_id=new.service_id).first():
                messages.error(request, "service exists")
                return redirect("services-dashboard")
            
        # print(new, id)
        if new is not None:
            
            new.service_id = request.POST.get("id")
            new.save()
            messages.success(request, "service edited")
            return redirect("services-dashboard")
        
        messages.error(request, "service edit failed")
        return redirect("services-dashboard")

    

def delete_service(request, id):
    # pass
    service = Service.objects.filter(id=id).first()
    
    if service is not None:
        service.delete()
        messages.success(request, "service deleted")
        return redirect("services-dashboard")
    
    messages.error(request, "failed to delete service")
    return redirect("services-dashboard")


def login_view(request):
    if request.POST:
        
        form = LoginForm(data=request.POST)
        if form.is_valid():
            
            # check if creds are true
            data = form.cleaned_data
            user = authenticate(email=data["email"], password=data["password"])
            if user is not None:
                user = User.objects.filter(email=data["email"]).first()
                print(user)
                login(request, user=user)
                context = {"user":user}
                messages.success(request, 'Login Successful Welcome to JAS, Janjas Auth System')
                return redirect('dashboard')
            
        messages.error(request, "Username or Password is incorrect")
        return redirect('login')
    
    context = {

    }
    return render(request, 'login_view.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'Bye bye!')
    return redirect('login')

