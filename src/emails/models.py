from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from users.models import User

# Create your models here.

def random_email_key(n=12):
    return get_random_string(n,"abcdefghijklmnopq123456789ABCDEFGHI")


class DynamicEmailConfiguration(models.Model):
    """
        Dynamic email configuration model
    """
    name = models.CharField(max_length=256, verbose_name = "email unique name", default=random_email_key())
    
    slug = models.SlugField(verbose_name = "slug", unique=True, default=slugify(name))
    
    created_by = models.ForeignKey(User, related_name="emails", verbose_name="creator", on_delete=models.CASCADE, default=1)
    
    email_key = models.CharField(max_length=1024, default=random_email_key())
    
    host = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = "Email Host", default='smtp.gmail.com')

    port = models.SmallIntegerField(
        blank = True, null = True,
        verbose_name = "Email Port", default=587)

    email_name = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = "Default From Email")

    username = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = "Email Authentication Username")

    password = models.CharField(
        blank = True, null = True,
        max_length = 256, verbose_name = "Email Authentication Password")

    use_tls = models.BooleanField(
        default = True, verbose_name = "Use TLS")

    use_ssl = models.BooleanField(
        default = False, verbose_name = "Use SSL")

    fail_silently = models.BooleanField(
        default = False, verbose_name = "Fail Silently")

    timeout = models.SmallIntegerField(
        blank = True, null = True,
        verbose_name = "Email Send Timeout (seconds)")

    def clean(self):
        if self.use_ssl and self.use_tls:
            raise ValidationError(
                "\"Use TLS\" and \"Use SSL\" are mutually exclusive, "
                "so only set one of those settings to True.")

    def save(self, *args, **kwargs):

        self.slug = slugify(self.email_name)

        key = random_email_key()
        self.email_key = key

        super(DynamicEmailConfiguration, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.slug} - {self.email_name}"

    class Meta:
        verbose_name = "Email Configuration"
