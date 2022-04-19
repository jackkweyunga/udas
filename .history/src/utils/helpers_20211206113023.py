from datetime import datetime

from django.utils import timezone
import math, random

from users.models import DynamicEmailConfiguration
from django.urls import reverse



def get_now() -> datetime:
    """
        returns the current date object
    """
    return timezone.now()


def generateOTP() :
    """
        function to generate OTP
    """
    # Declare a digits variable 
    # which stores all digits
    digits = "0123456789"
    OTP = ""
 
   # length of password can be changed
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
 
    return OTP



def get_configuration_admin_url(email_name):
    """
        returns dynamic email configurations
    """
    mod = DynamicEmailConfiguration.objects.filter(email_name=email_name).first()
    meta = DynamicEmailConfiguration._meta
    return reverse('admin:{}_{}_change'.format(
        meta.app_label, meta.model_name
    ), args=str(mod.id))

