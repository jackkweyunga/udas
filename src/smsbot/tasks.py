from celery import shared_task
from .twilio_send_sms import send_sms

@shared_task
def send_test_sms(bot_id, to, message="This is a test sms"):

    for t in to:
        try:
            send_sms(
                bot_id=bot_id,
                to=t.strip(),
                message_body=message
            )
        except:
            print("SMS Send Failed")
            