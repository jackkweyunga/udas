

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template import loader
from django.conf import settings

# from django.core.mail import send_mail
from utils.mail import send_mail
from emails.models import DynamicEmailConfiguration

subject = getattr(settings, 'DES_TEST_SUBJECT', "Test Email")
text_template = getattr(settings, 'DES_TEST_TEXT_TEMPLATE', "des/test_email.txt")
html_template = getattr(settings, 'DES_TEST_HTML_TEMPLATE', None)

message_text = loader.render_to_string(text_template)
message_html = loader.render_to_string(html_template) if html_template else None


@require_http_methods(["POST"])
def send_test_email(request, email_id):

    if request.user is None or not request.user.is_staff:
        return HttpResponseNotFound()

    emails = request.POST.get('emails', None).split(",")
    
    email_name = request.POST.get('email_name', None)

    config = DynamicEmailConfiguration.objects.filter(email_name=email_name).first()

    if emails:
        try:
            send_mail(
                subject,
                message_text,
                config.from_email or None,
                emails,
                html_message = message_html,
                email_name=email_name)

            messages.success(request, f"Test email sent. Please check \"{emails}\" for a message with the subject \"{subject}\"")
            
        except Exception as e:
            print(e)
            messages.error(request, f"Could not send email. {e}")
    else:
        messages.error(request, "You must provide an email address to test with.")

    return redirect('email', id=email_id)

