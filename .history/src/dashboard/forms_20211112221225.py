from django import forms
from auth

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("",)

    
