import json

data = json.load(open("data.json"))


def searchWord(word):
    word = word.lower()
    if word in data:
        return data[word]
    else:
        return None
