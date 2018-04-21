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
    # insertData - takes link, keywords, text and a doctype and writes link, text, keywords to main && link, keyword in keywords (each keyword is inserted seperatly)
    # insertDataInMain - just inserts the Data in main
    # insertDataInKeyword - just insert the Data in keywords
    def insertData(self, link, keywords, text, doctype):
        self.c.execute("INSERT INTO main VALUES (?,?,?)", (link, text, doctype))
        for keyword in keywords:
            self.c.execute("INSERT INTO keywords VALUES (?,?)", (link, keyword))

    def insertDataInMain(self, link, text, doctype):
        self.c.execute("INSERT INTO main VALUES (?,?,?)", (link, text, doctype))

    def insertDataInKeywords(self,link, keywords):
        for keyword in keywords:
            self.c.execute("INSERT INTO keywords VALUES (?,?)", (link, keyword))

    # Select
    # selectAllPreciseKeyword - enter an Keyword, check if the keyword is exactly in the tuple of keywords and returns the data from main
    # selectLinkPreciseKeyword - same as befor, but returns a link
    # selectALlIncludingKeyword - enter a Keyword, method check if keywords contain the entered keyword and returns all of main
    # selectLinkIncludingKeyword - same as before, but returns a link
    # selectAll(database) - SELECT * FROM database
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

    # update
    # updateMain(link, ("updateRow1", "updateRow2"), ("updateValue1","updateValue2"))
    #       - will update the given rows with the given values
    def updateMain(self,link, updatedRow, updateValue):
        if(len(updateValue)==len(updatedRow)):
            for i in range(0,len(updatedRow)-1):
                stmt = 'UPDATE main SET "{}" = "{}" WHERE link = "{}"'.format(updatedRow[i], updateValue[i],link)
                self.c.execute(stmt)

    # truncate the database
    def truncateDatabase(self, databasename):
        self.c.execute("DELETE FROM {}".format(databasename))
        return self.c.fetchall()

