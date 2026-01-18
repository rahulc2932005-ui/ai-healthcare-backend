import json, pickle, random

with open("intents.json") as f:
    intents = json.load(f)["intents"]

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def get_response(text):
    X = vectorizer.transform([text.lower()])
    tag = model.predict(X)[0]

    for intent in intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Sorry, I didn't understand. Please explain clearly."
