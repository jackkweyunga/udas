from django.core.mail import EmailMessage

from django.http import HttpResponse

from utils.token import default_token_generator
from django.templatetags.static import static

from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import set_cookie_with_token

# from janja_auth.models import DynamicEmailConfiguration

from users.models import DynamicEmailConfiguration, User
from utils.atomic_services import user_record_login
from django.template.loader import render_to_string
from utils import SITE

from users.models import RSAPair


# jwt login function
def jwt_login(*, response: HttpResponse, user: User) -> HttpResponse:

    """
        Log in with jwt token \n
        Returns a response carrying the token
    """
    
    keys = RSAPair.objects.first()

    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    jwt_public_key = keys.public
    jwt_private_key = keys.private
    jwt_algorithm = ''

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    if api_settings.JWT_AUTH_COOKIE:
        set_cookie_with_token(response, api_settings.JWT_AUTH_COOKIE, token)

    user_record_login(user=user)

    return response



# send email for verification
def send_email_for_verification(user, thread=True, **kwargs):
    """
        Sends email for verification of emails or accounts
    """

    redirect_url = kwargs.get("redirect_url")

    token, _ = default_token_generator.make_token(user)
    
    url = f"{SITE}/verify-email/{token}/?redirect_url={redirect_url}"

    config = DynamicEmailConfiguration.objects.filter(email_name="admin").first()

    email = EmailMessage(
        subject="Verify your email",
        body=render_to_string("email/verify_email.html", context={'url':url, 'user':user, "logo":f'{SITE}{static("img/logo-words.png")}'}),
        to=[user.email],
        from_email=config.from_email
    )

    email.content_subtype = 'html'
    email.send()



def send_email_for_password_reset(user, thread=True, **kwargs):

    """
        Sends email for password reset
    """

    redirect_url = kwargs.get("redirect_url")

    token, _ = default_token_generator.make_token(user)
    
    url = f"{SITE}/add-new-password/{token}/?redirect_url={redirect_url}"

    config = DynamicEmailConfiguration.objects.filter(email_name="admin").first()

    email = EmailMessage(
        subject="Janja Password reset",
        body=render_to_string("email/reset_password.html", context={'url':url, 'user':user, 'logo':f'{SITE}{static("img/logo-words.png")}'}),
        to=[user.email],
        from_email=config.from_email
    )

    email.content_subtype = 'html'
    email.send()

