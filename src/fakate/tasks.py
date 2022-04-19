from celery import shared_task
from .models import BotTrainingData
from .train_model import structure_training_data, train_model, vectorize_words
import time


def sync_train_model(botname):
    bot = BotTrainingData.objects.filter(botname=botname).first()

    if bot.intents != {}:

        data, encoded_intents = structure_training_data(data=bot.intents)

        x_data, vectorizer = vectorize_words(data["questions"])
        model = train_model(x_data, data["labels"])

        bot.model = model
        bot.vectorizer = vectorizer
        bot.labels = encoded_intents
        bot.save()

        return True

    return None


@shared_task
def async_save_labels(botname, labels):

    bot = BotTrainingData.objects.filter(botname=botname).first()
    
    if bot.labels != labels:
        bot.labels = labels
        bot.save()
        return labels
    elif bot.labels == labels:
        return "no changes"
    return None


@shared_task
def async_save_intents(botname, intents):

    bot = BotTrainingData.objects.filter(botname=botname).first()

    if bot.intents != intents:
        bot.intents = intents
        bot.save()
        time.sleep(1)
        sync_train_model(botname)

        return intents
    elif bot.intents == intents:
            return "no changes"

    return None


