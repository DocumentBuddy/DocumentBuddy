# import
import sqlite3


class Sqlite:

    def __init__(self):
        self.conn = sqlite3.connect('example.db')
        self.c = self.conn.cursor()

    def __init__(self, database_filename):
        self.conn = sqlite3.connect(database_filename)
        self.c = self.conn.cursor()

    # Close Connection
    def close_connection(self):
        self.conn.commit()
        self.conn.close()

    # Insert Data
    # insertData - takes link, keywords, text and a doctype and writes link, text, keywords to main && link, keyword in
    #   keywords (each keyword is inserted seperatly)
    # insertDataInMain - just inserts the Data in main
    # insertDataInKeyword - just insert the Data in keywords
    def insert_data(self, link, keywords, text, doctype):
        self.c.execute("INSERT INTO main VALUES (?,?,?)", (link, text, doctype))
        for keyword in keywords:
            self.c.execute("INSERT INTO keywords VALUES (?,?)", (link, keyword))

    def insert_data_in_main(self, link, text, doctype):
        self.c.execute("INSERT INTO main VALUES (?,?,?)", (link, text, doctype))

    def insert_data_in_keywords(self,link, keywords):
        for keyword in keywords:
            self.c.execute("INSERT INTO keywords VALUES (?,?)", (link, keyword))

    # Select
    # selectAllPreciseKeyword - enter an Keyword, check if the keyword is exactly in the tuple of keywords and returns
    #   the data from main
    # selectLinkPreciseKeyword - same as befor, but returns a link
    # selectALlIncludingKeyword - enter a Keyword, method check if keywords contain the entered keyword and returns all
    #   of main
    # selectLinkIncludingKeyword - same as before, but returns a link
    # selectAll(database) - SELECT * FROM database
    def select_all_precise_by_keyword(self, keyword):
        self.c.execute("SELECT * FROM main WHERE link = (SELECT link FROM keywords WHERE keyword=?)", (keyword,))
        return self.c.fetchall()

    def select_link_precise_by_keyword(self, keyword):
        self.c.execute("SELECT DISTINCT link FROM keywords WHERE keyword=?", (keyword,))
        return self.c.fetchall()

    def select_all_including_keyword(self, keyword):
        self.c.execute("SELECT * FROM main WHERE link = (SELECT link FROM keywords WHERE keyword LIKE ?)",
                       ('%' + keyword + '%',))
        return self.c.fetchall()

    def select_link_including_keyword(self, keyword):
        self.c.execute("SELECT DISTINCT link FROM keywords WHERE keyword LIKE ?", ('%' + keyword + '%',))
        return self.c.fetchall()

    def select_all(self, database_name):
        self.c.execute("SELECT * FROM {}".format(database_name))
        return self.c.fetchall()

    # update
    # updateMain(link, ("updateRow1", "updateRow2"), ("updateValue1","updateValue2"))
    #       - will update the given rows with the given values
    def update_main(self, link, updated_row, update_value):
        if len(update_value) == len(updated_row):
            for i in range(0, len(updated_row)-1):
                stmt = 'UPDATE main SET "{}" = "{}" WHERE link = "{}"'.format(updated_row[i], update_value[i], link)
                self.c.execute(stmt)

    # truncate the database
    def truncate_database(self, database_name):
        self.c.execute("DELETE FROM {}".format(database_name))
        return self.c.fetchall()
