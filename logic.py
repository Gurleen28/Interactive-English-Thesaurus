# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com

import json
import os
from database import Database
from difflib import get_close_matches

data = json.load(open(os.getcwd() + "\\data\\english_to_english.json"))


class Logic:
    def __init__(self):
        self.database = Database()

    def setupDatabase(self, username, password):
        engDict = generateDictLists()
        self.database.setLoginData(username, password)
        login = self.database.connect_database()
        self.database.create_database(engDict)
        return login

    def searchWord(self, word):
        definitions = ""
        if self.database.element_exists(word.lower()):                    # most words in database are lowercase
            definitions = self.database.getDefinitions(word.lower())
        elif self.database.element_exists(word):            # if words are written correctly (ex. correctly capitalized)
            definitions = self.database.getDefinitions(word)
        elif self.database.element_exists(word.capitalize()):             # capitals and countries
            definitions = self.database.getDefinitions(word.capitalize())
        elif self.database.element_exists(word.upper()):                  # USA and other acronyms
            definitions = self.database.getDefinitions(word.upper())

        if definitions:
            return self.optimizeDefinitions(definitions)
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
