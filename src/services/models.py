from django.db import models

from users.models import User
from django.core.management.utils import get_random_secret_key


# Create your models here.
####### services models

# microservices using the api
class Service(models.Model):
    """
        Services model.
    """
    service_id = models.CharField(max_length=25, unique=True)
    service_key = models.CharField( max_length=1024, default=get_random_secret_key)

    def refresh_key(self):
        self.service_key = get_random_secret_key()

    def __str__(self) -> str:
        return f"{self.service_id} - {self.service_key}"


class ServicePackage(models.Model):
    """
        Service subscription.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name}"


# package features
class PackageFeatures(models.Model):
    """
        Package feature
    """
    package = models.ForeignKey(ServicePackage, related_name="features", verbose_name="package", on_delete=models.CASCADE)
    feature = models.TextField()

    def __str__(self) -> str:
        return f"{self.package.name} - {self.id}"

# miccroservice Users.
class ServiceUser(models.Model):
    """
        Service user model
    """
    user = models.ForeignKey(User, related_name="services", verbose_name="user", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name="service_users", verbose_name="service", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.service.service_id} - {self.user.email} - {self.user.name}"

class ServiceUserSubscription(models.Model):
    """
        service users subscription
    """
    user = models.ForeignKey(User, related_name="subscriptions", verbose_name="subscriber", on_delete=models.CASCADE)
    package = models.ForeignKey(ServicePackage, related_name="package_users", verbose_name="package", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.package.name}"
