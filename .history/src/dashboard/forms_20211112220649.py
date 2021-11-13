from django import forms


class AddUserForm(forms.class Form(forms.ModelForm):
    
    class Meta:
        model = 
        fields = ("",)
):
    email = forms.EmailField(max_length=44)
    password = forms.CharField(max_length=44)
    
