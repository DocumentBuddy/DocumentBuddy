# import
import sqlite3

class Sqlite:
    def __init__(self):
        self.conn = sqlite3.connect('example.db')
        self.c = self.conn.cursor()

    def __init__(self, databasename):
        self.conn = sqlite3.connect(databasename)
        self.c = self.conn.cursor()

    # Close Connection
    def closeConnection(self):
        self.conn.commit()
        self.conn.close()

    # Insert Data
    def insertData(self, link, keywords, text, doctype):
        self.c.execute("INSERT INTO main VALUES (?,?,?)", (link, text, doctype))
        for keyword in keywords:
            self.c.execute("INSERT INTO keywords VALUES (?,?)", (link, keyword))


    # Select
    def selectAllPreciseByKeyword(self, keyword):
        self.c.execute("SELECT * FROM main WHERE link = (SELECT link FROM keywords WHERE keyword=?)", (keyword,))
        return self.c.fetchall()


    def selectLinkPreciseByKeyword(self, keyword):
        self.c.execute("SELECT DISTINCT link FROM keywords WHERE keyword=?", (keyword,))
        return self.c.fetchall()


    def selectAllIncludingKeyword(self, keyword):
        self.c.execute("SELECT * FROM main WHERE link = (SELECT link FROM keywords WHERE keyword LIKE ?)",
                       ('%' + keyword + '%',))
        return self.c.fetchall()


    def selectLinkIncludingKeyword(self, keyword):
        self.c.execute("SELECT DISTINCT link FROM keywords WHERE keyword LIKE ?", ('%' + keyword + '%',))
        return self.c.fetchall()


    def selectAll(self, databasename):
        self.c.execute("SELECT * FROM {}".format(databasename))
        return self.c.fetchall()


    def truncateDatabase(self, databasename):
        self.c.execute("DELETE FROM {}".format(databasename))
        return self.c.fetchall()

