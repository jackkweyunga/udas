from django import forms
from 

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("",)

    
