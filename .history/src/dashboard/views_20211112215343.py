from django.shortcuts import render
from django.http import V

# Create your views here.
class IndexView(View):
    
    def get(self, requesst):
        