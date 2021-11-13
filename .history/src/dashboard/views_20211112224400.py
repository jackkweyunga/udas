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

    
        