import json
import wx
import GUI
from difflib import get_close_matches

data = json.load(open("data.json"))

def generateDictList(language):
    if language == "english":
        engDict = []
        for k, v in data.items():
            for i in range(0, len(v)):
                engDict.append((k, v[i]))
    return engDict


def searchWord(word, frame):
    if word.lower() in data:             # most words in database are lowercase
        return data[word.lower()]
    elif word in data:                   # if words are written correctly (ex. correctly capitalized)
        return data[word]
    elif word.capitalize() in data:      # capitals and countries
        return data[word.capitalize()]
    elif word.upper() in data:           # USA and other acronyms
        return data[word.upper()]
    # add intelligent search
    elif len(get_close_matches(word, data.keys(), n=3, cutoff=0.8)) > 0:
        matches = get_close_matches(word, data.keys(), n=3, cutoff=0.8)
        dialog = GUI.ChoiceDialog(frame, matches)
        return ""
    else:
        return "Word not found."
