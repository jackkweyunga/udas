from email.policy import default
from django.db import models
from picklefield.fields import PickledObjectField


d_intents = {
    "Intents": {
        "salamu": {
            "Questions": [
                "Habari",
                "Hi"
            ],
            "Answers": [
                "Karibu Fukate"
            ]
        },
        "shukrani": {
            "Questions": [
                "Asante"
            ],
            "Answers": [
                "Karibu tena."
            ]
        },
        "daktari": {
            "Questions": [
                "Daktari"
            ],
            "Answers": [
                "Aina gani ya daktari. \n",
                "1. Binafsi \n",
                "2. Umma"
            ]
        }
    },
    "Options": {
        "daktari": {
            "1": [
                "daktari binafsi"
            ],
            "2": [
                "daktari wa umma"
            ]
        }
    }
}

d_labels = {"0": "salamu", "1": "shukrani", "2": "daktari"}


class BotTrainingData(models.Model):
    botname = models.CharField(max_length=1024, unique=True)
    labels = models.JSONField(null=False, default=d_labels)
    intents = models.JSONField(null=False, default=d_intents)
    model = PickledObjectField(null=True)
    vectorizer = PickledObjectField(null=True)

    def __str__(self) -> str:
        return f"{self.botname}"

        
