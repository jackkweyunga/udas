from django.db import models

# Create your models here.


class TwilioAccountSettings(models.Model):
    twilio_account_name = models.CharField(max_length=1024)
    twilio_account_sid = models.CharField(max_length=1024)
    twilio_auth_token = models.CharField(max_length=1024)

    def __str__(self) -> str:
        return f"{self.twilio_account_name}"


class TwilioPhoneNumbers(models.Model):
    settings = models.ForeignKey(TwilioAccountSettings, related_name="phone_numbers", on_delete=models.CASCADE, default=1)
    number = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.number}"
