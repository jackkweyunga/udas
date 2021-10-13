
# imports

from django.urls.base import reverse_lazy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


## Root API

@api_view(['GET'])
def api_root(request, format=None):
    """
        A root api view
    """
    return Response({
        "api_version":"1.0.0",
        "documentaion":"_url_"
        },)

## authentication API

# register user
class UserRegistrationApiView():
    """
        User Api View class
    """
    pass


# login user
class LoginUserApiView():
    """
        Login User Api View
    """
    pass


# get logged in user
class GetLoggedInUSerApiView():
    """
        Get Logged in user Api View
    """
    pass


# logout user 
class LogoutUserApiView():
    """
        Logout user Api View
    """
    pass


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
