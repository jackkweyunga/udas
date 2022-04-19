from django import forms
from users.models import User

class UserCreationUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email","username")


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()
