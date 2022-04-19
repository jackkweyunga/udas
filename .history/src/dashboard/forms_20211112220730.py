from django import forms


class UserForm(forms.ModelForm):
    
    class Meta:
        model = U
        fields = ("",)

    
