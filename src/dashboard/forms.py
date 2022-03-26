from django import forms
from users.models import User
from emails.models import DynamicEmailConfiguration, random_email_key

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
        exclude = ['slug','timeout','fail_silently','use_ssl','use_tls','api_key','created_by', 'email_key']

    def save(self, commit: bool = ...):
        self.email_key = random_email_key()
        return super().save(commit)

