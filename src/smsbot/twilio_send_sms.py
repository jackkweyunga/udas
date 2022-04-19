
from .models import TwilioPhoneNumbers
from twilio.rest import Client


def send_sms(bot_id, message_body, to):

    bot = TwilioPhoneNumbers.objects.filter(id = bot_id).first()
    TWILIO_ACCOUNT_SID = bot.settings.twilio_account_sid
    TWILIO_AUTH_TOKEN = bot.settings.twilio_auth_token
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages \
                .create(
                     body = message_body,
                     from_ = bot.number,
                     to=to
                 )
    return message.status