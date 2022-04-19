from django import forms


class AddUserForm(forms.ModeFo):
    email = forms.EmailField(max_length=44)
    password = forms.CharField(max_length=44)
    
