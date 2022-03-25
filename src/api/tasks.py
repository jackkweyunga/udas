
from celery import shared_task
from utils.mail import EmailMessage
from utils.atomic_services import log


@shared_task
def send_email(email, email_name, from_email, to):
    
    success = []
    failures = []

    for address in email["to"]:
        try:
            e_msg = email
            e_msg["to"] = address 
            emailmsg = EmailMessage(**email)
            emailmsg.content_subtype = 'html'
            emailmsg.send()
            success.append(address)
        except:
            failures.append(address)

    log(f"Email sending success FROM: {email_name} - {from_email}  to LIST:{success}", model="email")
    log(f"Email sending failed FROM: {email_name} - {from_email}  to LIST:{failures}", model="email")





