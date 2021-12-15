
## imports

# builtin
import os
from urllib.parse import urlencode
from requests.api import post
import random

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
from django.urls.base import reverse_lazy

# custom
from utils.mixins import PublicApiMixin, ApiAuthMixin, ApiErrorsMixin
from utils.atomic_services import user_before_create, user_change_secret_key
from utils.services import jwt_login, user_record_login, SITE
from utils.helpers import generateOTP
from utils.selectors import user_get_me
from users.models import RSAPair
from users.models import User, DynamicEmailConfiguration
from utils.mail import EmailMessage

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
            },
            "rsa":{
                "get_public_key":request.build_absolute_uri(reverse('api:rsa:get_public_key'))
            }
        }
        },)
    
## RSA keys

# get a public key for a given private key
class RSAPublicKey(APIView):
    """RSA Public Key"""
    
    def get(self, request):
        
        pair = random.choice(RSAPair.objects.all())
        
        payload = {
            "id": pair.id,
            "key": pair.public_key
        }
        
        return Response(payload, status=status.HTTP_200_OK)


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
    queryset = User
    
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
        
        Post template 
        
        {
            "subject":"",
            "body": [
                "p> A paragraph \n",
                "a> a link t>> link text \n",
                "b> a link button t>> link text \n"
            ]
            "recipient_list":[""],
            "emailer_name":"admin",
            "api_key":"the key here"
        }
        
        
    """  
    class EmailSerializer(serializers.Serializer):
        subject = serializers.CharField()
        body = serializers.ListField()
        template_type = serializers.CharField()
        recipient_list = serializers.ListField()
        emailer_name = serializers.CharField(required=False, default='admin')
        api_key = serializers.CharField()

    def post(self, request):

        serializer = self.EmailSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        emailer_name = validated_data.get('emailer_name') or None
        key = validated_data.get('api_key') or None
        config = DynamicEmailConfiguration.objects.filter(email_name="admin").first()
        
        if emailer_name != None:
            config = DynamicEmailConfiguration.objects.filter(email_name=f"{emailer_name}", api_key=key).first()
            if not config:
                data = {
                    'message': f'The name {emailer_name} with key provided is not registered as an emailer. Plz visit your developers console to create one.',
                    'status': status.HTTP_404_NOT_FOUND,
                    }
                return Response(data, status=data['status'])

        to = validated_data.get('recipient_list')
        template_type = validated_data.get('template_type')
        email_body = validated_data.get('body')
        
        EMAIL_TEMPLATE_TYPES = {
            "follow_up": "email/custom_templates/follow_up_email_template.html"
        }
        
        EMAIL_BODY_SYNTAX = {
                    "p>":["<p>","**","</p>"],
                    "a>":["<a href='","****","'>","**","</a>"],
                    "b>":["<a href='","****","'><button style='padding:10px;border-radius:10px;cursor:pointer;background:#0061f2;color:#ffffff;'>","**","</button></a>"],
                    "span>":["<span>","**","</span>"],
                }
                
                
        new  = []
        for i in email_body:
            
            ii = i
            k =i
            for key in EMAIL_BODY_SYNTAX.keys():
                
                all_tags = [f"<{m}" for m in EMAIL_BODY_SYNTAX.keys() ]
                
                if len(i.strip().split(key)) > 1:
                                        
                    # check for duplicates
                    if i.strip().split(key)[0] in all_tags:
                        print(i.strip().split(key)[0])
                        
                    else:
                        tt = i.strip().split(key)[1]
                        print(" was here", EMAIL_BODY_SYNTAX[key])
                        ind = EMAIL_BODY_SYNTAX[key].index("**")
                        print(ind)
                        kk = [ v for v in EMAIL_BODY_SYNTAX[key]]
                        kk[ind] = tt
                        ii = "".join(kk) 
                        
                        if f"<{key}" in ["<a>","<b>"]:
                            if len(k.split("href>")) > 1:
                                _tt = k.split("href>")[1].strip()
                                print(tt, _tt)
                                kk[ind] = tt.split(f"href> {_tt}")[0]
                                ii = "".join(kk) 
                                href_pos = ii.split("****")
                                href_pos.insert(1,_tt)
                                ii = "".join(href_pos) 
                            
                            
                        
                elif len(i.split(key)) == 1:
                    if i.split("<p>")[0] == " " and i.split(key)[0] not in all_tags:
                        ii = "".join(["<p>",f"{i}","</p>"])
            k = None
            new.append(ii)
                    
        email_body = "\n".join(new)

    
        if len(to) == 1 and EMAIL_TEMPLATE_TYPES[template_type]:
            
            email = EmailMessage(
                subject = validated_data.get('subject'),
                body = loader.render_to_string(EMAIL_TEMPLATE_TYPES[template_type] , {"name":f"{to[0]}", "email_name":f"{emailer_name}", "body":email_body }),
                to = to,
                from_email=config.from_email,
                email_name=emailer_name
            )
            
            # example
        """
            {
            "subject":"Testing",
            "body": [
            "p> Hello",
            "p> You are receing this email as a test. Using a simple syntax, links and buttons cab be encorporated in emails via the janjas api.",
            "b> This is a link button to janjas.tk href> https://janjas.tk",
            "p> Below is a link",
            "a> This is a link to janjas.tk href> https://janjas.tk"
            ],
            "recipient_list":["jackkweyunga@gmail.com"],
            "emailer_name":"admin",
            "template_type":"follow_up",
            "api_key":"eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluQGV4YW1wbGUuY29tIiwiaWF0IjoxNjM4ODY0ODkzLCJleHAiOjE2NDE0OTI4OTMsImp0aSI6IjVlMzFjODlkLTQxMTYtNDRmYy05MjQwLWMwMDczNzI3MjZlOCIsInVzZXJfaWQiOjEsIm9yaWdfaWF0IjoxNjM4ODY0ODkzfQ.olJW2Obr6dtNNHyI703P7_0l0hAyWAcE2hRjz_ROL4AmEUmcgljZ0WQOH_dx4uBGslfEkiHuAkvsddGWTljzECe0ZPKvas8PFJKR18ebjYuKnPo_vi0Nc0DcSdLw88uPu85P7NeXz_l3KM4pwmu1TTiq6dHfjmuwIQaao6zvqS4LbNfxl17006TrpDpR9gBP1NZe_XSmUfmw1BwkDAV0V8CywTZTQPWYofPysBN9ISCnyO4C0DZj_hieS3nyRnL-jVmgnIF4OdawDSeXF8wJZzG7Di3SowVQvXmyYXOt1f_SZtt6J_ltGGfTK_A7lki4A6ESNnr8k1dglYCF6lJrsA"
            }
        """

        email.content_subtype = 'html'
        
        try:
            email.send()  
        except Exception as e:
            
            data = {
                    'message': f'something is wrong. Did you provide correct recepient emails',
                    'status': status.HTTP_404_NOT_FOUND,
                    }
            
            return Response(data, status=data['status'])
            

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
        
        Post template
        
        {
            "number":"+255"
        }
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

