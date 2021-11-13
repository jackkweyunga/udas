from django import forms
from users.models import User

class UserCreUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email","username")

    
