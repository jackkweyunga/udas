

from django.conf import settings
import django
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "auth.settings"

django.setup()

# from users.models import User
from django.contrib.auth.models import User

def createSuperUser( password, username="admin", email = "admin@example.com", firstName = "", lastName = ""):

    try:
        user = User.objects.get(username="admin")
        return None
    except:
        pass

    user = User(
        username = username,
        email = email,
        first_name = firstName,
        last_name = lastName,
    )
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user

createSuperUser("changeme")

