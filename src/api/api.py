
# imports


from urllib.parse import urlencode
from django.templatetags.static import static
from requests.api import post

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.views import ObtainJSONWebTokenView

from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect, render

from django.urls.base import reverse_lazy
from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.reverse import reverse
from django.http import JsonResponse
from utils.mixins import *
from utils.atomic_services import *
from utils.services import *
from selectors import *
from utils.helpers import *
from utils.selectors import *

## Root API

@api_view(['GET'])
def api_root(request, format=None):
    """
        A root api view
    """
    return JsonResponse({
        "api_version":"1.0.0",
        "documentaion":"_url_"
        },)



## authentication API

# register user
class UserRegistrationApiView(PublicApiMixin, ApiErrorsMixin, APIView):
    
    """
        User Api View class
    """
    
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        phone = serializers.CharField()
        first_name = serializers.CharField(required=False, default='')
        last_name = serializers.CharField(required=False, default='')
        password = serializers.CharField()

    def post(self, request, *args, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**serializer.validated_data)

        response = Response(data=user_get_me(user=user))
        response = jwt_login(response=response, user=user)

        return response


# login user
class LoginUserApiView(ApiErrorsMixin, ObtainJSONWebTokenView):

    """
        Login User Api View
    """
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        x = serializer.is_valid(raise_exception=True)

        logged_in_user = request.user if request.user.is_authenticated else None
        user = serializer.validated_data.get('user') or logged_in_user
        user_record_login(user=user)

        return super().post(request, *args, **kwargs)


# get logged in user
class GetLoggedInUSerApiView(ApiAuthMixin, ApiErrorsMixin, APIView):
    """
        Get Logged in user Api View
    """

    def get(self, request, *args, **kwargs):
        return Response(user_get_me(user=request.user))


# logout user 
class LogoutUserApiView(ApiAuthMixin, ApiErrorsMixin, APIView):
    """
        Logout user Api View
    """
    
    def post(self, request):
        """
        Logs out user by removing JWT cookie header.
        """
        user_change_secret_key(user=request.user)

        response = Response(status=status.HTTP_202_ACCEPTED)
        response.delete_cookie(settings.JWT_AUTH['JWT_AUTH_COOKIE'])

        return response


# deactivate user
class DeactivateUserApiView():
    """
        Deactivate User Api View
    """
    pass


## Email API

# send email verification msg (otp)
class SendVerificationEmailApiView():
    """
        Send Verification Email Api View
    """
    pass

# verify otp
class VerifyOTPApiView():
    """
        Verify OTP Api View
    """
    pass

# change password email (otp)
class ChangePasswordEmailApiView():
    """
        Change Password Email Api View
    """
    pass


# confirm changed password with otp
class ConfirmChangedPasswordApiView():
    """
        Confirm Changed Password Api View
    """
    pass


## Phone API

# update phone number
class UpdatePhoneNumber():
    """
        Update Phone Number Api View
    """
    pass

# send otp to verify phone number
class SendOTPApiView():
    """
        Send OTP Api View
    """
    pass

# verify sent otp
class VerifySentOTPApiView():
    """
        Verify Sent OTP Api View
    """
    pass
