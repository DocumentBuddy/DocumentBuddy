# import
import os
import sqlite3
import itertools


class Sqlite:
    def __init__(self, database_path=None):
        if database_path is None:
            database_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'example.db'
            )
        self.conn = sqlite3.connect(database_path)
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
    def insert_data(self, link, keywords, text, doctype, toc, author, name_entities, pages, date):
        print((link, text, doctype, toc, author, pages, date,))
        print(len((link, text, doctype, toc, author, pages, date,)))
        self.c.execute("INSERT INTO main (link, text, doctype, toc, author, pages, date) VALUES (?,?,?,?,?,?,?)",
                           (link, text, doctype, toc, author, pages, date,))
        self.c.execute("SELECT max(id) FROM main")
        id=self.c.fetchone()
        for keyword in keywords:
            self.c.execute('INSERT INTO keywords (id, keyword) VALUES ("{}" , "{}")'.format(id[0],keyword))
        for name_entity in name_entities:
            self.c.execute('INSERT INTO names (id, name) VALUES ("{}" , "{}")'.format(id[0],name_entity))

    def insert_data_in_main(self, link, text, doctype, toc, author, name_entities, pages, date):
        self.c.execute("INSERT INTO main (link, text, doctype, toc, author, pages, date) VALUES (?,?,?,?,?,?,?)",
                           (link, text, doctype, toc, author, pages, date))
        for name_entity in name_entities:
            self.c.execute('INSERT INTO names (id, name) VALUES ("{}" , "{}")'.format(id[0],name_entity))

    def insert_data_in_keywords(self, id, keywords):
        for keyword in keywords:
            self.c.execute('INSERT INTO keywords (id,keyword) VALUES ("{}","{}")'.format(id, keyword))

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

    def select_all_including_name(self, name):
        self.c.execute("SELECT * FROM main WHERE id IN (SELECT DISTINCT id FROM names WHERE name LIKE ?)", ('%' + name + '%',))
        return self.c.fetchall()

    def select_all_precise_by_name(self, name):
        self.c.execute('SELECT * FROM main WHERE id IN (SELECT id FROM names WHERE name="{}")'.format(name))
        return self.c.fetchall()

    # Select more keywords
    def select_from_keywords(self, keywords):
        data =[]
        for keyword in keywords:
            self.c.execute("SELECT DISTINCT id FROM keywords WHERE keyword LIKE ?", ('%' + keyword + '%',))
            data.append(self.c.fetchall())
            data = list(itertools.chain.from_iterable(data))
            data = [list(i) if isinstance(i, tuple) else [i] for i in data]
            newdata = []
            for d in data:
                newdata.append(d[0])
        newdata=list(set(newdata))
        return_data = []
        for item in newdata:
            self.c.execute("SELECT * FROM main WHERE ID = ?", (item,))
            return_data.append(self.c.fetchone())
        return return_data

    #select any database
    def select_all(self, database_name):
        self.c.execute("SELECT * FROM {}".format(database_name))
        return self.c.fetchall()

    # select id returns main
    def select_from_id(self, id):
        self.c.execute("SELECT * FROM main WHERE id=?",(id,))
        return self.c.fetchall()

    # select id returns link
    def select_link_from_id(self, id):
        self.c.execute("SELECT link FROM main WHERE id=?", (id,))
        return self.c.fetchone()[0]

    # select author
    def select_like_from_author(self, author):
        self.c.execute("SELECT * FROM main WHERE author LIKE ?", ('%' + author + '%',))
        return self.c.fetchall()

    # select doctype
    def select_like_from_doctype(self, doctype):
        self.c.execute("SELECT * FROM main WHERE doctype LIKE ?", ('%' + doctype + '%',))
        return self.c.fetchall()

    def select_text_from_id(self, id):
        self.c.execute("SELECT text FROM main WHERE id = ?",(id,))
        return self.c.fetchone()

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

    # create Tables
    def create_table_main(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS main (ID INTEGER PRIMARY KEY AUTOINCREMENT, link text, text text,"
                       " doctype text, toc text, author text, pages INTEGER, date text)")

    def create_table_keywords(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS keywords (id INTEGER, keyword text, "
                       "FOREIGN KEY(id) REFERENCES main(ID), PRIMARY  KEY (id, keyword))")

    def create_table_names(self):
        self.c.execute("CREATE TABLE IF NOT EXISTS names (id INTEGER, name text, "
                       "FOREIGN KEY(id) REFERENCES main(ID), PRIMARY  KEY (id, name))")

    # Drop Tables
    def drop_table(self, database_name):
        self.c.execute("DROP TABLE IF EXISTS {}".format(database_name))