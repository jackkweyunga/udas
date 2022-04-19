from django.urls import path, include
from api.api import *


authentication_patterns = [

    # register user
    path('register/', UserRegistrationApiView.as_view(), name="register"),

    # login user
    path('login/', LoginUserApiView.as_view(), name="login"),

    # get logged in user
    path('me/', GetLoggedInUSerApiView.as_view(), name="me"),

    # logout user 
    path('logout/', LogoutUserApiView.as_view(), name="logout"),

    # register a non-login user
    path('register_non_login_user/', RegisterNonLoginUserApiView.as_view(), name="register_non_login_user" ),

    # deactivate user
    path('deactivate/', DeactivateUserApiView.as_view(), name="deactivate"),

    # activate user
    path('activate/', ActivateUserApiView.as_view(), name="activate")
]

email_patterns = [

    # send email
    path('send_email/', SendEmailApiView.as_view(), name="send_email"),

    # send email verification msg (otp)
    path('send_verification_email/', SendVerificationEmailApiView.as_view(), name="send_verification_email"),

    # verify otp
    path("verify_email_otp", VerifyEmailSentOTPApiView.as_view(), name="verify_email_otp"),

    # change password email (otp)
    path("send_change_password_otp", ChangePasswordEmailApiView.as_view(), name="send_change_password_otp"),

    # confirm changed password with otp
    path("confirm_changed_password", ConfirmChangedPasswordApiView.as_view(), name="confirm_changed_password"),

    # change meail 
    path("change_email", ChangeEmailApiView.as_view(), name="change_email"),

]


phone_patterns = [

    # send sms
    path("send_sms/", SendSMSApiView.as_view(), name="send_sms"),

    # update phone number
    path('update_phone/', UpdatePhoneNumber.as_view(), name="update_phone"),

    # send otp to verify phone number
    path("send_otp/", SendSMSOTPApiView.as_view(), name="send_otp"),

    # verify sent otp
    path("verify_otp/", VerifySMSSentOTPApiView.as_view(), name="verify_otp")

]


rsa_patterns = [
    # get rsa public key
    path("s")
]

app_name = 'api'

urlpatterns = [
    path('auth/', include((authentication_patterns, 'auth'))),
    path('email/', include((email_patterns, 'email'))),
    path('phone/', include((phone_patterns, 'phone'))),
    path('', api_root, name='api-root'),
]


