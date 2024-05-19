import random
import json
import torch
from flask import request

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("intents.json", "r", encoding="utf-8") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"


def get_response(msg, db_cursor):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                if tag == "average_pulse":
                    user_email = request.headers.get("Authorization")
                    if user_email:
                        user_email = user_email.split(" ")[1]
                        db_cursor.execute(
                            "SELECT AVG(heart_rate) FROM health_data WHERE user_email = %s", (user_email,)
                        )
                        average_pulse = db_cursor.fetchone()[0]
                        if average_pulse is not None:
                            average_pulse = round(average_pulse, 1)
                            return f"Your average pulse rate is {average_pulse} beats per minute."
                        else:
                            return "No pulse data available."
                    else:
                        return "Authorization header is missing"
                elif tag == "user_count":
                    db_cursor.execute("SELECT COUNT(*) FROM users")
                    user_count = db_cursor.fetchone()[0]
                    return f"There are {user_count} users registered in the system."
                elif tag == "minimal_pulse":
                    user_email = request.headers.get("Authorization")
                    if user_email:
                        user_email = user_email.split(" ")[1]
                        db_cursor.execute(
                            "SELECT MIN(heart_rate) FROM health_data WHERE user_email = %s", (user_email,)
                        )
                        minimal_pulse = db_cursor.fetchone()[0]
                        if minimal_pulse is not None:
                            minimal_pulse = round(minimal_pulse, 1)
                            return f"The minimum recorded pulse rate is {minimal_pulse} beats per minute."
                        else:
                            return "No pulse data available."
                    else:
                        return "Authorization header is missing"
                elif tag == "maximal_pulse":
                    user_email = request.headers.get("Authorization")
                    if user_email:
                        user_email = user_email.split(" ")[1]
                        db_cursor.execute(
                            "SELECT MAX(heart_rate) FROM health_data WHERE user_email = %s", (user_email,)
                        )
                        maximal_pulse = db_cursor.fetchone()[0]
                        if maximal_pulse is not None:
                            maximal_pulse = round(maximal_pulse, 1)
                            return f"The maximum recorded pulse rate is {maximal_pulse} beats per minute."
                        else:
                            return "No pulse data available."
                    else:
                        return "Authorization header is missing"
                else:
                    return random.choice(intent["responses"])

    return "I do not understand..."
