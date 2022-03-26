

from django.http import HttpResponseNotFound
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template import loader
from django.conf import settings

# from django.core.mail import send_mail
from emails.tasks import async_send_email
from emails.models import DynamicEmailConfiguration
from utils.email_templates import FollowUpEmailTemplate


@require_http_methods(["POST"])
def send_test_email(request, email_id):

    if request.user is None or not request.user.is_staff:
        return HttpResponseNotFound()

    emails = request.POST.get('emails', None).split(",")
    
    name = request.POST.get('name', None)

    config = DynamicEmailConfiguration.objects.filter(name=name).first()

    if emails:
        try:
            subject = "Test Email"
            message_text = "This is a test email. Seems every thing is working fine."
            body = FollowUpEmailTemplate(
                message_text,
                config.name,
                config.email_name,
            ).load_template()

            async_send_email(
                subject=subject,
                body=body,
                to=emails,
                email_configuration_name=config.name,
                email_configuration_email_name=config.email_name
            )

            messages.success(request, f"Test email sent. Please check \"{emails}\" for a message with the subject \"{subject}\"")
            
        except Exception as e:
            print(e)
            messages.error(request, f"Could not send email. {e}")
    else:
        messages.error(request, "You must provide an email address to test with.")

    return redirect('email', id=email_id)

