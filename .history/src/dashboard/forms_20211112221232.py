from django import forms
from auth.m

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("",)

    
