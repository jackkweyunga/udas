from django.contrib import admin
from .models import PackageFeatures, Service, ServicePackage, ServiceUser, ServiceUserSubscription

# Register your models here.
admin.site.register([
PackageFeatures, Service, ServicePackage, ServiceUser, ServiceUserSubscription
])