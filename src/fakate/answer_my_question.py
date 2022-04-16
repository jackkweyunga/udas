import json
import joblib
import pathlib

from fakate.models import BotTrainingData

# ========= load vectorizer and model ================

def v_m(botname):
    bot = BotTrainingData.objects.filter(botname=botname).first()

    if bot:
        return bot.vectorizer, bot.model, bot.labels, bot.intents

    return None


def construct_answer(botname, intent):
    _, _, _, intents = v_m(botname)
    return "".join(intents["Intents"][intent]["Answers"])


def answer_now(botname, message):
    vectorizer, model, label_to_intent, intent = v_m(botname)
    # print(label_to_intent, intent)
    my_question = vectorizer.transform([message]).toarray()
    label = model.predict(my_question)[0]
    intent = label_to_intent.get(str(label))
    return intent, construct_answer(botname, intent)


def answer_options(botname, intent, option_number):
    _, _, _, intents = v_m(botname)
    return "".join(intents["Options"][intent][str(option_number)])


# print(answer_now("Hi"))

