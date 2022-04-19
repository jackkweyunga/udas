

from django.contrib.sites.models import Site
from django.db import OperationalError

try:
    SITE = Site.objects.get_current()
except:
    SITE = ""