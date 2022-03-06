from django.shortcuts import render, redirect
from django.views import View 
from users.models import SystemLogs, User, DynamicEmailConfiguration, Service, ServicePackage, ServiceUser, ServiceUserSubscription
from utils.atomic_services import user_create
from utils.mixins import LoginRequired
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, EmailConfigCreateForm
# Create your views here.

class IndexView(LoginRequired, View):
    
    """ Index View """  
    
    def get(self, request):
        
        context = {
            "services":Service.objects.all(),
            "user":request.user,
            "n_users":User.objects.all().count(),
            "n_emails":DynamicEmailConfiguration.objects.all().count(),
            "n_services": Service.objects.all().count(),
            "sys_logs": SystemLogs.objects.all(),
        }
        return render(request, "dashboard/index.html", context=context)

class EmailsView(LoginRequired, View):
    
    def get(self, request):
        
        all = DynamicEmailConfiguration.objects.all()
        
        context = {
            "emails":all,
            "count":all.count()
        }
        
        return render(request, 'dashboard/emails.html', context)
    
    
    def post(self, request):
        
        form = EmailConfigCreateForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                email = DynamicEmailConfiguration.objects.filter(**form.cleaned_data).first()
                email.created_by = request.user()
                messages.success(request, 'email settings added')
            except:
                messages.success(request, form.errors.as_text())
                
        else:
            messages.error(request, 'failed to create email settings')
        
        return redirect('emails')
    
    
class email_view(LoginRequired, View):
    
    def get(self, request, id):
        email = DynamicEmailConfiguration.objects.filter(id=id).first()
        
        if email.email_key == '':
            from rest_framework_jwt.utils import uuid
            from django.utils.crypto import get_random_string
            
            key = uuid.uuid1(node=int(id), clock_seq=1)
            key = get_random_string(12,"abcdefghijklmnopq123456789ABCDEFGHI")
            email.email_key = key
            email.save()
        
        context = {
            "email": email,
        }
        
        return render(request, 'dashboard/email_view.html', context=context)
    
    
    def post(Self, request, id):
        data = request.POST.dict()
        print(data)
        
        email = DynamicEmailConfiguration.objects.filter(id = id).first()
        print(email)
        
        if email:
            # edit settings
            email.email_name = data.get('email_name')
            email.host = data.get('host')
            email.port = data.get('port')
            email.from_email = data.get('from_email')
            email.username = data.get('username')
            email.password = data.get('password')
            email.save()
            messages.success(request, 'settings saved succesfully ')
        else:
            messages.error(request, 'failed to edit email settings')
        
        return redirect('email', id=email.id)
    
    
class UsersView(LoginRequired, View):
    
    def get(self, request):
        
        all = User.objects.all()
        context = {
            
            "users":all,
            "count":all.count()
            
        }
        
        return render(request, 'dashboard/users.html', context)
    
    def post(Self, request):
        
        first_name = request.POST["firstname"]
        last_name = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        
        user, err = user_create(email, password, first_name=first_name, last_name=last_name, phone=phone)
        
        if user is not None:
            messages.info(request, "User created successful")
            return redirect("users-dashboard")
        
        messages.info(request, err)
        return redirect("users-dashboard")


class UserDeleteView(DeleteView):
    model = User
    success_url = "/dashboard/users/"

        
        
    
@login_required
def user_view(request, id):
    
    context = {
        "selected_user":User.objects.filter(id=id).first()
    }
    
    return render(request, 'dashboard/user_view.html', context)

    
class ServicesView(LoginRequired, View):
    
    def get(self, request):
        all = Service.objects.all()
        context = {
            "services":all,
            "count": all.count()
        }
        
        return render(request, 'dashboard/services.html', context)


class add_service(LoginRequired, View):
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

class edit_service(LoginRequired, View):
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

    
@login_required
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


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Bye bye!')
    return redirect('login')

