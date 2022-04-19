
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django.utils.translation import gettext_lazy as _

from users.models import *
from django.forms import ModelForm, PasswordInput


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    """
        User Admin class
    """

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','phone')}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email', )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')


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


admin.site.register([
    Service,
    ServicePackage,
    PackageFeatures,
    ServiceUser,
    ServiceUserSubscription,
])

    
@admin.register(RSAPair)
class RSAPairAdmin(admin.ModelAdmin):
    readonly_fields = ["public_key","private_key"]



