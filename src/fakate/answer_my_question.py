import json
import joblib
import pathlib

# ========= load vectorizer and model ================

dir = pathlib.Path(__file__).parent

vectorizer = joblib.load(dir / "vectorizer.pkl")
model = joblib.load(dir / "model.pkl")


# ======== load the label to intent =================

label_to_intent = json.load(open(dir / "label_to_intents.json"))


# ========= load the akiba.json ======================

master_json = json.load(open(dir / "fakate.json"))


def construct_answer(intent):
    return "".join(master_json["Intents"][intent]["Answers"])


def answer_now(message):
    my_question = vectorizer.transform([message]).toarray()
    label = model.predict(my_question)[0]
    intent = label_to_intent.get(str(label))
    return intent, construct_answer(intent)


def answer_options(intent, option_number):
    return "".join(master_json["Options"][intent][str(option_number)])


# print(answer_now("Hi"))

