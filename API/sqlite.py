# import
import sqlite3
import itertools


class Sqlite:
    def dict_factory(self, row):
        d = {}
        for idx, col in enumerate(self.c.description):
            d[col[0]] = row[idx]
        return d

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
    def insert_data(self, link, keywords, text, doctype, toc, author, pages, date):
        self.c.execute("INSERT INTO main (link, text, doctype, toc, author, pages, date) VALUES (?,?,?,?,?,?,?)", (link, text, doctype, toc, author, pages, date))
        self.c.execute("SELECT max(id) FROM main")
        id=self.c.fetchone()
        for keyword in keywords:
            self.c.execute('INSERT INTO keywords (id, keyword) VALUES ("{}" , "{}")'.format(id[0],keyword))

    def insert_data_in_main(self, link, text, doctype, toc, author, pages, date):
        self.c.execute("INSERT INTO main (link, text, doctype, toc, author, pages, date) VALUES (?,?,?,?,?,?,?)", (link, text, doctype, toc, author, pages, date))

    def insert_data_in_keywords(self, id, keywords):
        for keyword in keywords:
            self.c.execute('INSERT INTO keywords (id,keyword) VALUES ("{}","{}")', (id, keyword))

    # Select
    # selectAllPreciseKeyword - enter an Keyword, check if the keyword is exactly in the tuple of keywords and returns
    #   the data from main
    # selectLinkPreciseKeyword - same as befor, but returns a link
    # selectALlIncludingKeyword - enter a Keyword, method check if keywords contain the entered keyword and returns all
    #   of main
    # selectLinkIncludingKeyword - same as before, but returns a link
    # selectAll(database) - SELECT * FROM database
    def select_all_precise_by_keyword(self, keyword):
        self.c.execute('SELECT * FROM main WHERE id IN (SELECT id FROM keywords WHERE keyword="{}")'.format(keyword))
        return self.c.fetchall()

    def select_link_precise_by_keyword(self, keyword):
        self.c.execute("SELECT DISTINCT id FROM keywords WHERE keyword=?", (keyword,))
        return self.c.fetchall()

    def select_all_including_keyword(self, keyword):
        self.c.execute("SELECT * FROM main WHERE id IN (SELECT id FROM keywords WHERE keyword LIKE ?)",
                       ('%' + keyword + '%',))
        return self.c.fetchall()

    def select_link_including_keyword(self, keyword):
        self.c.execute("SELECT DISTINCT id FROM keywords WHERE keyword LIKE ?", ('%' + keyword + '%',))
        return self.c.fetchall()

    def select_all(self, database_name):
        self.c.execute("SELECT * FROM {}".format(database_name))
        return self.c.fetchall()

    # Select more keywords
    def select_from_keywords(self, keywords):
        self.conn.row_factory = self.dict_factory
        data =[]
        for keyword in keywords:
            self.c.execute("SELECT DISTINCT id FROM keywords WHERE keyword LIKE ?", ('%' + keyword + '%',))
            data.append(self.c.fetchall())
            data = list(itertools.chain.from_iterable(data))
            data = [list(i) if isinstance(i, tuple) else [i] for i in data]
            newdata = []
            for d in data:
                newdata.append(d[0])
        return newdata

    # Select doctype

    # update
    # updateMain(link, ("updateRow1", "updateRow2"), ("updateValue1","updateValue2"))
    #       - will update the given rows with the given values
    # def update_main(self, id, updated_row, update_value):
    #    if len(update_value) == len(updated_row):
    #        for i in range(0, len(updated_row)-1):
    #            stmt = 'UPDATE main SET "{}" = "{}" WHERE id = "{}"'.format(updated_row[i], update_value[i], id)
    #            self.c.execute(stmt)

    # truncate the database
    def truncate_database(self, database_name):
        self.c.execute("DELETE FROM {}".format(database_name))
        return self.c.fetchall()

    def create_table_main(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS main (ID INTEGER PRIMARY KEY AUTOINCREMENT, link text, text text,"
                       " doctype text, toc text, author text, pages INTEGER, date text)")

    def create_table_keywords(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS keywords (id INTEGER, keyword text, FOREIGN KEY(id) REFERENCES main(ID))")

    def drop_table(self, database_name):
        self.c.execute("DROP TABLE IF EXISTS {}".format(database_name))