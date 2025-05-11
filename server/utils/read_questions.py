import json

def read_questions():
    with open("server/questions.json", "r") as f:
        return json.load(f)
