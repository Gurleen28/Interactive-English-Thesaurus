import psycopg2 as pg


class Database:
    def __init__(self):
        self.conn = pg.connect(
            "dbname='postgres' user='postgres' password='postgresgurleen' host='127.0.0.1' port='5432'")  # dictDb
        self.conn.autocommit = True
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("CREATE DATABASE dictDb;")
        except pg.errors.DuplicateDatabase:
            print("Database already exists")
        self.cur.execute("DROP TABLE IF EXISTS english")
        self.cur.execute("CREATE TABLE english (word TEXT, definition TEXT)")

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
