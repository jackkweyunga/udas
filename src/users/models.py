from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key

from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class User(AbstractUser):

    """
        A custom user model
    """

    username = None
    phone = models.CharField(max_length=250, null=True, blank=True)

    email = models.EmailField(unique=True, db_index=True)
    secret_key = models.CharField(max_length=255, default=get_random_secret_key)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    class Meta:
        swappable = 'AUTH_USER_MODEL'

    @property
    def name(self):
        """
            Returns a full name
        """
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'



class DynamicEmailConfiguration(models.Model):
    """
        Dynamic email configuration model
    """
    email_name = models.CharField(unique=True, max_length=256, verbose_name = _("email unique name"))
    slug = models.SlugField(verbose_name = _("slug"), unique=True, default=slugify(email_name))
    host = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = _("Email Host"), default='smtp.gmail.com')

    port = models.SmallIntegerField(
        blank = True, null = True,
        verbose_name = _("Email Port"), default=587)

    from_email = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = _("Default From Email"))

    username = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = _("Email Authentication Username"))

    password = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = _("Email Authentication Password"))

    use_tls = models.BooleanField(
        default = True, verbose_name = _("Use TLS"))

    use_ssl = models.BooleanField(
        default = False, verbose_name = _("Use SSL"))

    fail_silently = models.BooleanField(
        default = False, verbose_name = _("Fail Silently"))

    timeout = models.SmallIntegerField(
        blank = True, null = True,
        verbose_name = _("Email Send Timeout (seconds)"))

    def clean(self):
        if self.use_ssl and self.use_tls:
            raise ValidationError(
                _("\"Use TLS\" and \"Use SSL\" are mutually exclusive, "
                "so only set one of those settings to True."))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.email_name)
        super(DynamicEmailConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return _(f"{self.slug}")

    class Meta:
        verbose_name = _("Email Configuration")




