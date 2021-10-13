from django.urls import path, include
from api.api import api_root


authentication_patterns = [

    # register user

    # login user

    # get logged in user

    # logout user 

    # deactivate user
]



email_patterns = [

    # send email verification msg (otp)

    # verify otp

    # change password email (otp)

    # confirm changed password with otp

]


phone_patterns = [

    # update phone number

    # send otp to verify phone number

    # verify sent otp

]

app_name = 'api'

urlpatterns = [
    path('auth/', include((authentication_patterns, 'auth'))),
    path('email/', include((email_patterns, 'email'))),
    path('phone/', include((phone_patterns, 'phone'))),
    path('', api_root, name='api-root'),
]


