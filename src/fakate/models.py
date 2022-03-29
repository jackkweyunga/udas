from django.db import models

class BotTrainingData(models.Model):
    botname  = models.CharField(max_length=1024)
    labels = models.JSONField(null=True)
    intents = models.JSONField(null=True)

    def __str__(self) -> str:
        return f"{self.botname}"
