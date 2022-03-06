from celery.utils.log import get_task_logger
from celery import shared_task
from utils.mail import EmailMessage
from utils.atomic_services import log


@shared_task
def send_email(email, email_name, from_email, to):
    
    try:
        emailmsg = EmailMessage(**email)
        emailmsg.content_subtype = 'html'
        # log(f"Email sending success FROM: {email_name} - {from_email}  to LIST:{to}", model="email")
        emailmsg.send()
    except:
        # log(f"Email sending failed FROM: {email_name} - {from_email}  to LIST:{to}", model="email")
        pass


@shared_task
def add(x,y):
    return x+y



