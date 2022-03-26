from django.contrib import admin
from emails.models import DynamicEmailConfiguration
from django.forms import ModelForm, PasswordInput


# Register your models here.


class DynamicEmailConfigurationForm(ModelForm):
    class Meta:
        model = DynamicEmailConfiguration
        exclude = ['slug']
        widgets = {
            "password": PasswordInput(render_value=True),
        }


class DynamicEmailConfigurationAdmin(admin.ModelAdmin):
    form = DynamicEmailConfigurationForm
    change_form_template = 'des/change_form.html'
    class Media:
        js = ('js/des.js'),
        css = {
            'all': ('css/des.css',)
        }

admin.site.register(DynamicEmailConfiguration, DynamicEmailConfigurationAdmin)