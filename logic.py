import json
import database
import GUI
from difflib import get_close_matches

data = json.load(open("data\\english_to_english.json"))

def generateDictLists():
    engDict = []
    for k, v in data.items():
        for i in range(0, len(v)):
            engDict.append((k, v[i]))
    return engDict


def searchWord(word, frame):
    if database.getDefinitions(word.lower()):              # most words in database are lowercase
        return optimizeDefinitions(database.getDefinitions(word.lower()), frame)
    elif database.getDefinitions(word):                    # if words are written correctly (ex. correctly capitalized)
        return optimizeDefinitions(database.getDefinitions(word), frame)
    elif database.getDefinitions(word.capitalize()):       # capitals and countries
        return optimizeDefinitions(database.getDefinitions(word.capitalize()), frame)
    elif database.getDefinitions(word.upper()):            # USA and other acronyms
        return optimizeDefinitions(database.getDefinitions(word.upper()), frame)
    # add intelligent search
    elif len(get_close_matches(word, data.keys(), n=3, cutoff=0.8)) > 0:
        matches = get_close_matches(word, data.keys(), n=3, cutoff=0.8)
        dialog = GUI.ChoiceDialog(frame, matches)
        return ""
    else:
        return "Word not found."

def optimizeDefinitions(mydefs, frame):
    result = ""
    for i in range(0, len(mydefs)):
        result += str(i + 1) + ". " + mydefs[i] + "\n"
    if i >= 4:
        frame.Maximize()
    return result

