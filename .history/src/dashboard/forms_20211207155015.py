from django import forms
from users.models import User, DynamicEmailConfiguration

class UserCreationUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email","password")


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


class EmailConfigCreateForm(forms.ModelForm):
    
    class Meta:
        model = DynamicEmailConfiguration
        
    def save(self, data):
        