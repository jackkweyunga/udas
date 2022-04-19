from django import forms


class AddUserForm(forms.Mode):
    email = forms.EmailField(max_length=44)
    password = forms.CharField(max_length=44)
    
