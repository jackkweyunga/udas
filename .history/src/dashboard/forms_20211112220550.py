from django import forms


class AddUserForm(forms.Form):
    email = forms.EmailField(max_length=44)
    