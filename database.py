import psycopg2 as pg

def createTable(name):
    conn = pg.connect("dbname='dictDb' user='postgres' password='postgresgurleen' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS " + name + "(word TEXT, definition TEXT)")
    conn.commit()
    conn.close()

# rows is a list containing tuples (word, definition)
def insertElements(table, rows):
    # safety measure
    if len(rows) < 1:
        return
    conn = pg.connect("dbname='dictDb' user='postgres' password='postgresgurleen' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.executemany("INSERT INTO " + table + " VALUES (%s, %s)", rows)
    conn.commit()
    conn.close()

def getDefinitions(word):
    conn = pg.connect("dbname='dictDb' user='postgres' password='postgresgurleen' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM english WHERE word=%s", (word,))
    rows = cur.fetchall()
    definitions = [i[1] for i in rows]
    conn.close()
    return definitions