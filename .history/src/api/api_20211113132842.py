
## imports

# builtin
import os
from urllib.parse import urlencode
from requests.api import post

# rest
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# rest jwt
from rest_framework_jwt.views import ObtainJSONWebTokenView

# django
from django.template import loader
from django.urls import reverse
from django.conf import settings
from django.templatetags.static import static
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.http import JsonResponse

# custom
from utils.mixins import *
from utils.atomic_services import *
from utils.services import *
from utils.helpers import *
from utils.selectors import *
from utils.rsa impo

# twilio
from twilio.rest import Client



## Root API

@api_view(['GET'])
def api_root(request, format=None):

    """
        A root api view
    """

    return Response({
        "api_version":"1.0.0",
        "documentaion":"_url_",
        "endpoints":{
            "auth":{
                "login":request.build_absolute_uri(reverse("api:auth:login")),
                "register":request.build_absolute_uri(reverse("api:auth:register")),
                "logged_in_user":request.build_absolute_uri(reverse("api:auth:me")),
                "logout":request.build_absolute_uri(reverse("api:auth:logout")),
                "register_non_login_user":request.build_absolute_uri(reverse("api:auth:register_non_login_user")),
                "deacivate":request.build_absolute_uri(reverse("api:auth:deactivate")),
                "acivate":request.build_absolute_uri(reverse("api:auth:activate"))
            },
            "email":{
                "send_email":request.build_absolute_uri(reverse('api:email:send_email')),
                "send_verification_email":request.build_absolute_uri(reverse('api:email:send_verification_email')),
                "verify_email_otp":request.build_absolute_uri(reverse('api:email:verify_email_otp')),
                "send_change_password_otp":request.build_absolute_uri(reverse('api:email:send_change_password_otp')),
                "confirm_changed_password":request.build_absolute_uri(reverse("api:email:confirm_changed_password")),
                "change_email":request.build_absolute_uri(reverse("api:email:change_email")),

            },
            "phone":{
                "send_sms":request.build_absolute_uri(reverse('api:phone:send_sms')),
                "update_phone":request.build_absolute_uri(reverse('api:phone:update_phone')),
                "send_otp":request.build_absolute_uri(reverse('api:phone:send_otp')),
                "verify_otp":request.build_absolute_uri(reverse('api:phone:verify_otp'))
            }
        }
        },)
    
## RSA keys

# get a public key for a given private key
class RSAPublicKey(APIView):
    """RSA Public Key"""
    
    def get(self, request):
        
        return 


## authentication API

# register non login user
class RegisterNonLoginUserApiView(APIView):
    """
        Api view to register users who dont need to login \n
        Such as customers, Lenders, So on
    """

# register user
class UserRegistrationApiView(PublicApiMixin, ApiErrorsMixin, APIView):

    """
        User Api View class
    """
    
    class InputSerializer(serializers.Serializer):
        services = serializers.ListField()
        email = serializers.EmailField()
        phone = serializers.CharField()
        first_name = serializers.CharField()
        last_name = serializers.CharField()
        password = serializers.CharField()


    def post(self, request, *args, **kwargs):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_before_create(**serializer.validated_data)
        if user == None:
            response = Response(data={
                "error":"user with this email exists"
            })
            return response

        if user == "phone exists":
            response = Response(data={
                "error":"user with this phone exists"
            })
            return response

        response = Response(data={
            "user":user_get_me(user=user),
            "services":[]
        })
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
class DeactivateUserApiView(APIView):

    """
        Deactivate User Api View
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):

        ser = self.InputSerializer(data = request.data)
        data = ser.is_valid(raise_exception=True)

        if data:
            email = ser.validated_data["email"]
            user = User.objects.filter(email=email).first()

            if user:
                user.is_active = False
                user.save()
                response = Response(data={"message"f"user with email {email} has been deactivaed"})
                return response

            response = Response(data={"error":"the email is not registered"})

            return response


# activate user
class ActivateUserApiView(APIView):

    """
        Activate User Api View
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    def post(self, request):

        ser = self.InputSerializer(data = request.data)
        data = ser.is_valid(raise_exception=True)
        # print(data)

        if data:
            email = ser.validated_data.get("email")
            user = User.objects.filter(email=email).first()
            # print(user, email)
            if user:
                user.is_active = True
                user.save()
                response = Response(data={"message"f"user with email {email} has been activated"})
                return response
      
            response = Response(data={"error":"the email is not registered"})

            return response
    


## Email API

# send email
class SendEmailApiView(PublicApiMixin, ApiErrorsMixin, APIView):
    """
        send a custom email
    """  
    class EmailSerializer(serializers.Serializer):
        subject = serializers.CharField()
        body = serializers.CharField()
        recipient_list = serializers.ListField()
        emailer_name = serializers.CharField(required=False, default='admin')

    def post(self, request):

        serializer = self.EmailSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        emailer_name = validated_data.get('emailer_name') or None
        config = DynamicEmailConfiguration.objects.filter(email_name="admin").first()
        
        if emailer_name != None:
            config = DynamicEmailConfiguration.objects.filter(email_name=f"{emailer_name}").first()
            if not config:
                data = {
                    'message': f'The name {emailer_name} is not registered as an emailer. Plz visit your developers console to create one.',
                    'status': status.HTTP_404_NOT_FOUND,
                    }
                return Response(data, status=data['status'])

        email = EmailMessage(
            subject = validated_data.get('subject'),
            body = validated_data.get('body'),
            to = validated_data.get('recipient_list'),
            from_email=config.from_email
        )  

        email.content_subtype = 'html'
        email.send()  

        data = {
        'message': 'Email sent!',
        'status': status.HTTP_200_OK,
        }

        return Response(data, status=status.HTTP_200_OK)


# send email verification msg (otp)
class SendVerificationEmailApiView(SendEmailApiView):
    """
        Send Verification Email Api View
    """
    class EmailSerializer(serializers.Serializer):
        email = serializers.EmailField()
        emailer_name = serializers.CharField(required=False, default='admin')

    def post(self, request):
        serializer = self.EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        email = validated_data["email"]
        otp = generateOTP()
        # send email

        data = {
            'message': 'Email sent!',
            'email': email,
            'otp': otp,
            'status': status.HTTP_200_OK,
        }

        emailer_name = validated_data.get('emailer_name') or None
        config = DynamicEmailConfiguration.objects.filter(email_name="admin").first()

        msg = EmailMessage(
            subject="janjas OTP",
            to=[email],
            body=loader.render_to_string("email/otp_email.html", context={'otp':otp, "logo":f'{SITE}{static("img/logo-words.png")}'}),
            from_email=config.from_email
        )  

        msg.content_subtype = 'html'
        msg.send()  

        return Response(data, status=status.HTTP_200_OK)


# verify otp
class VerifyEmailSentOTPApiView(APIView):
    """
        Verify OTP Api View
    """
    pass

# change password email (otp)
class ChangePasswordEmailApiView(APIView):
    """
        Change Password Email Api View
    """
    pass


# confirm changed password with otp
class ConfirmChangedPasswordApiView(APIView):
    """
        Confirm Changed Password Api View
    """
    pass

# change email
class ChangeEmailApiView(APIView):
    """
        Change email Api view
    """
    pass


## Phone API

# send sms
class SendSMSApiView(APIView):

    """
        Send sms Api View
    """

    pass

# update phone number
class UpdatePhoneNumber(APIView):
    """
        Update Phone Number Api View
    """
    pass

# send otp to verify phone number
class SendSMSOTPApiView(PublicApiMixin, ApiErrorsMixin, APIView):
    """
        Send OTP Api View
    """
    
    class SendSerializer(serializers.Serializer):
        number = serializers.CharField(required=False)


    def post(self, request):

        input_serializer = self.SendSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        print(validated_data)

        code = validated_data.get('code')
        type = validated_data.get('type')
        number = validated_data.get('number')

        account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
        auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)
        
        verification = client.verify \
            .services(settings.TWILIO["SERVICE_ID"]) \
            .verifications \
            .create(to=number, channel='sms')
        return Response({'status':verification.status})

# verify sent otp
class VerifySMSSentOTPApiView(PublicApiMixin, ApiErrorsMixin, APIView):
    """
        Verify Sent OTP Api View
    """
    class VerifySerializer(serializers.Serializer):
        number = serializers.CharField(required=False)
        code = serializers.CharField(required=False)

    def post(self, request):
    
        input_serializer = self.VerifySerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        print(validated_data)

        code = validated_data.get('code')
        type = validated_data.get('type')
        number = validated_data.get('number')

        account_sid = settings.TWILIO['TWILIO_ACCOUNT_SID']
        auth_token = settings.TWILIO['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
            .services(settings.TWILIO["SERVICE_ID"]) \
            .verification_checks \
            .create(to=number, code= code)
        return Response({'status':verification_check.status})


## services API

