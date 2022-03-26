from django.shortcuts import redirect, render
from django.views import View

from utils.mixins import LoginRequired
from smsbot.tasks import send_test_sms
# Create your views here.

class SendTestSmsView(View, LoginRequired):
    
    def post(self, request):

        bot_id = request.POST["bot_id"]
        to = request.POST["to"]

        send_test_sms.delay(
            bot_id=bot_id,
            to=to,
        )

        return redirect("smsbot", id=bot_id)