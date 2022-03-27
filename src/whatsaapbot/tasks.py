from celery import shared_task
from twilio.rest import Client
from smsbot.models import TwilioPhoneNumbers

@shared_task
def send_whatsaap_message(phone_number_id):

    phone_number = TwilioPhoneNumbers.objects.filter(id=phone_number_id).first()

    client = Client(phone_number.settings.twilio_account_sid, phone_number.settings.twilio_auth_token)

    client.messages \
    .create(
         media_url=['https://images.unsplash.com/photo-1545093149-618ce3bcf49d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=668&q=80'],
         from_="whatsapp:"+phone_number.number,
         to='whatsapp:+255712111936'
    )



