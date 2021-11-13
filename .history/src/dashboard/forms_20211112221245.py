from django import forms
from users.models import 

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("",)

    
