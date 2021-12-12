

from django.core.mail.message import EmailMultiAlternatives, EmailMessage

from django.utils.module_loading import import_string
from django.conf import settings
from utils.email_backend import ConfiguredEmailBackend

def get_connection(backend=None, fail_silently=False, email_name=None, **kwds):
    """Load an email backend and return an instance of it.

    If backend is None (default), use settings.EMAIL_BACKEND.

    Both fail_silently and other keyword arguments are used in the
    constructor of the backend.
    """
    klass = ConfiguredEmailBackend
    return klass(fail_silently=fail_silently, email_name=email_name, **kwds)



# overwritting EmailMessage
class EmailMessage(EmailMessage):
    
    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
                 connection=None, attachments=None, headers=None, cc=None,
                 reply_to=None):
        super().__init__(subject, body, from)
    
    def get_connection(self, fail_silently=False):
        if not self.connection:
            self.connection = get_connection(fail_silently=fail_silently)
        return self.connection




def send_mail(subject, message, from_email, recipient_list,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None, html_message=None, email_name=None):
    """
    Easy wrapper for sending a single message to a recipient list. All members
    of the recipient list will see the other recipients in the 'To' field.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
        email_name=email_name
    )
    mail = EmailMultiAlternatives(subject, message, from_email, recipient_list, connection=connection)
    if html_message:
        mail.attach_alternative(html_message, 'text/html')

    return mail.send()


def send_mass_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    """
    Given a datatuple of (subject, message, from_email, recipient_list), send
    each message to each recipient list. Return the number of emails sent.

    If from_email is None, use the DEFAULT_FROM_EMAIL setting.
    If auth_user and auth_password are set, use them to log in.
    If auth_user is None, use the EMAIL_HOST_USER setting.
    If auth_password is None, use the EMAIL_HOST_PASSWORD setting.

    Note: The API for this method is frozen. New code wanting to extend the
    functionality should use the EmailMessage class directly.
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    messages = [
        EmailMessage(subject, message, sender, recipient, connection=connection)
        for subject, message, sender, recipient in datatuple
    ]
    return connection.send_messages(messages)