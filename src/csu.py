

from django.conf import settings
import django
import os
from users.models import User

# some settings
os.environ["DJANGO_SETTINGS_MODULE"] = "auth.settings"
django.setup()



def createSuperUser( password="changeme", email = "admin@example.com", firstName = "Admin", lastName = "User"):
    """
        A function to create a django default super user
    """
    try:
        user = User.objects.get(email=email)
        return None
    except:
        pass

    user = User(
        email = email,
        first_name = firstName,
        last_name = lastName,
    )
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user


# A function call to create a default super user whenever the function is called.
createSuperUser()

