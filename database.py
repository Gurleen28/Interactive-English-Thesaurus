# @author Gurleen Kour
# Permission to copy and modify all files if author is credited
# email: gurleenkour2800@gmail.com


import psycopg2 as pg
import psycopg2.errors as pge


class Database:

    def setLoginData(self, username, password):
        self.username = username
        self.password = password

    def connect_database(self):
        try:
            self.conn = pg.connect(
                "dbname='postgres' user='" + self.username + "' password='" + self.password + "' host='127.0.0.1' port='5432'")
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
            return True
        except pge.OperationalError:
            return False  # login unsuccessful

    def create_database(self, engDict):
        try:
            self.cur.execute("CREATE DATABASE dictDb;")
            self.cur.execute("DROP TABLE IF EXISTS english")
            self.cur.execute("CREATE TABLE english (word TEXT, definition TEXT)")
            self.insertElements("english", engDict)
            print("New database dictDb created")
        except pge.DuplicateDatabase:
            print("Database dictdB already exists")

    # rows is a list containing tuples (word, definition)
    def insertElements(self, table, rows):
        # safety measure
        if len(rows) < 1:
            return
        self.cur.executemany("INSERT INTO " + table + " VALUES (%s, %s)", rows)

    def getDefinitions(self, word):
        self.cur.execute("SELECT * FROM english WHERE word=%s", (word,))
        rows = self.cur.fetchall()
        definitions = [i[1] for i in rows]
        return definitions

    def element_exists(self, word):
        self.cur.execute("SELECT definition FROM english WHERE word = %s", (word,))
        return self.cur.fetchone() is not None

