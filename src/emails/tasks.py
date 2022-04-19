
from celery import shared_task
from utils.mail import EmailMessage
from utils.atomic_services import log


class CustomEmail:
    
    def __init__(self, subject, body, to, email_configuration_name) -> None:
        self.subject = subject
        self.body = body

        if isinstance(to, list):
            self.to = to
        else: 
            raise TypeError("'To' : must be a list of email addresses")

        self.email_configuration_name = email_configuration_name

    def __str__(self) -> str:
        return f"{self.subject}"


@shared_task
def async_send_email(subject, body, to, email_configuration_name, email_configuration_email_name):
    
    success = []
    failures = []

    email = CustomEmail(
        subject=subject,
        body=body,
        to=to,
        email_configuration_name=email_configuration_name,
    )

    for address in email.to:
        # try:
        e_msg = email
        email.to = list([address]) 
        emailmsg = EmailMessage(**email.__dict__)
        emailmsg.content_subtype = 'html'
        emailmsg.send()
        success.append(address)
    #     except:
    #         failures.append(address)

    # if len(success) > 0:
    #     log(f"Email sending success FROM: {email_configuration_name} - {email_configuration_email_name}  to LIST:{success}", model="email")
    
    # if len(failures) > 0:
    #     log(f"Email sending failed FROM: {email_configuration_name} - {email_configuration_email_name}  to LIST:{failures}", model="email")



