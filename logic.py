import json
from database import Database
from difflib import get_close_matches

data = json.load(open("data\\english_to_english.json"))


class Logic:
    def __init__(self):
        self.database = Database()
        engDict = generateDictLists()
        self.database.insertElements("english", engDict)

    def searchWord(self, word):
        if self.database.getDefinitions(word.lower()):  # most words in database are lowercase
            return self.optimizeDefinitions(self.database.getDefinitions(word.lower()))
        elif self.database.getDefinitions(word):  # if words are written correctly (ex. correctly capitalized)
            return self.optimizeDefinitions(self.database.getDefinitions(word))
        elif self.database.getDefinitions(word.capitalize()):  # capitals and countries
            return self.optimizeDefinitions(self.database.getDefinitions(word.capitalize()))
        elif self.database.getDefinitions(word.upper()):  # USA and other acronyms
            return self.optimizeDefinitions(self.database.getDefinitions(word.upper()))
        else:
            return ""

    def getCloseMatches(self, word):
        # add intelligent search
        if len(get_close_matches(word, data.keys(), n=3, cutoff=0.8)) > 0:
            matches = get_close_matches(word, data.keys(), n=3, cutoff=0.8)
            return matches

    def optimizeDefinitions(self, mydefs):
        result = ""
        for i in range(0, len(mydefs)):
            result += str(i + 1) + ". " + mydefs[i] + "\n"
        return result


def generateDictLists():
    engDict = []
    for k, v in data.items():
        for i in range(0, len(v)):
            engDict.append((k, v[i]))
    return engDict
