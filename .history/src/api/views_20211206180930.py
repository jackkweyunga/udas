
from django.http import HttpResponseRedirect, HttpResponseNotFound, r
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
from users.models import DynamicEmailConfiguration

subject = getattr(settings, 'DES_TEST_SUBJECT', _("Test Email"))
text_template = getattr(settings, 'DES_TEST_TEXT_TEMPLATE', "des/test_email.txt")
html_template = getattr(settings, 'DES_TEST_HTML_TEMPLATE', None)

message_text = loader.render_to_string(text_template)
message_html = loader.render_to_string(html_template) if html_template else None


@require_http_methods(["POST"])
def send_test_email(request):

    if request.user is None or not request.user.is_staff:
        return HttpResponseNotFound()

    emails = request.POST.get('emails', None).split(",")
    
    emailer_name = request.POST.get('emailer_name', None)

    config = DynamicEmailConfiguration.objects.filter(email_name=emailer_name).first()

    if emails:
        try:
            send_mail(
                subject,
                message_text,
                config.from_email or None,
                emails,
                html_message = message_html)

            messages.success(request,
                    _("Test email sent. Please check \"{}\" for a "
                    "message with the subject \"{}\"").format(
                    emails,
                    subject
                )
            )
        except Exception as e:
            messages.error(request, _("Could not send email. {}").format(e))
    else:
        messages.error(request, _("You must provide an email address to test with."))

    return HttpResponseRedirect()

