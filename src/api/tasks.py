
from celery import shared_task
from utils.mail import EmailMessage
from utils.atomic_services import log


@shared_task
def send_email(email, email_name, from_email, to):
    
    try:
        emailmsg = EmailMessage(**email)
        emailmsg.content_subtype = 'html'
        emailmsg.send()
        log(f"Email sending success FROM: {email_name} - {from_email}  to LIST:{to}", model="email")
    except:
        log(f"Email sending failed FROM: {email_name} - {from_email}  to LIST:{to}", model="email")





