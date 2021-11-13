from django import forms
from users.models import Mo

class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("",)

    
