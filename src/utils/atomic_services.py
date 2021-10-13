from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key
from django.contrib.auth.hashers import check_password

from utils import get_now

from users.models import User


def user_create(email, password=None, **extra_fields) -> User:
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
        'is_active': False,
        **extra_fields
    }

    user = User(email=email, **extra_fields)

    if password:
        user.set_password(password)

        # verify user email or phone number.

    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user

def user_create_superuser(email, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields,
        'is_staff': True,
        'is_superuser': True
    }

    user = user_create(email=email, password=password, **extra_fields)

    return user


def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()

    return user


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:

        user = User.objects.filter(email=email).first()

        if user:
            return user, False

        return user_create(email=email, **extra_data), True
    

@transaction.atomic
def user_get_full(username):
    user = User.objects.filter(email=username).first()

    return {
        'name': user.name,
        'email': user.email
    }

@transaction.atomic
def user_get_by_password(email, password):
    try:
        user = User.objects.filter(email=email).first()
        if user and check_password(password, user.password):
            return user
    except:
        return None


@transaction.atomic
def user_get_by_email(email):
    try:
        user = User.objects.filter(email=email).first()
        return user
    except:
        return None

# for users using google.
@transaction.atomic
def user_add_password(data):
    try:
        user = User.objects.filter(email=data["email"]).first()
        user.phone = data["phone"]
        user.is_active = True
        user.set_password(data["password"])
        user.save()
        return user
    except:
        return None




        