import json
# import joblib
import pandas as pd
from pandas.core.algorithms import mode
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer


def structure_training_data(data):
    intents = data["Intents"].keys()
    encoded_intents = {index: intent for index, intent in enumerate(intents)}
    reversed_intents = {intent: index for index, intent in encoded_intents.items()}
    x_data = []
    y_data = []
    for intent in intents:
        ntent_data = data["Intents"][intent]["Questions"]
        labels = [reversed_intents[intent]] * len(ntent_data)
        x_data.extend(ntent_data)
        y_data.extend(labels)

    # with open(f"label_to_intents.json", "w") as f:
    #     json.dump(encoded_intents, f)

    data = pd.DataFrame(list(zip(x_data, y_data)), columns=["questions", "labels"])
    return data, encoded_intents


def vectorize_words(x_data):
    vectorizer = TfidfVectorizer()
    x_data = vectorizer.fit_transform(x_data).toarray()

    # ============== storing the vectorizer to file =======================
    # joblib.dump(vectorizer, "vectorizer.pkl")

    return x_data, vectorizer


def train_model(x_data, labels):
    model = RandomForestClassifier()
    model.fit(x_data, labels)

    # ============== storing the model to file ============================
    # joblib.dump(model, "model.pkl")

    return model


# data = structure_training_data()
# x_data = vectorize_words(data["questions"])
# model = train_model(x_data, data["labels"])


