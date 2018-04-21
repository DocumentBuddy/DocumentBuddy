# import
import pprint
import sqlite3


# Connection to Database
def openconnection(dbfilename):
    conn = sqlite3.connect(dbfilename)
    c = conn.cursor()
    return [conn, c]


# Close Connection
def closeConnection(connection):
    connection.commit()
    connection.close()


# Insert Data
def insertData(cursor, link, keywords, text, doctype):
    cursor.execute("INSERT INTO main VALUES (?,?,?)", (link, text, doctype))
    for keyword in keywords:
        cursor.execute("INSERT INTO keywords VALUES (?,?)", (link, keyword))


# Select
def selectAllPreciseByKeyword(cursor, keyword):
    cursor.execute("SELECT * FROM main WHERE link = (SELECT link FROM keywords WHERE keyword=?)", (keyword,))
    return cursor.fetchall()


def selectLinkPreciseByKeyword(cursor, keyword):
    cursor.execute("SELECT DISTINCT link FROM keywords WHERE keyword=?", (keyword,))
    return cursor.fetchall()


def selectAllIncludingKeyword(cursor, keyword):
    cursor.execute("SELECT * FROM main WHERE link = (SELECT link FROM keywords WHERE keyword LIKE ?)",
                   ('%' + keyword + '%',))
    return cursor.fetchall()


def selectLinkIncludingKeyword(cursor, keyword):
    cursor.execute("SELECT DISTINCT link FROM keywords WHERE keyword LIKE ?", ('%' + keyword + '%',))
    return cursor.fetchall()


def selectAll(cursor, databasename):
    cursor.execute("SELECT * FROM {}".format(databasename))
    return cursor.fetchall()


def truncateDatabase(cursor, databasename):
    cursor.execute("DELETE FROM {}".format(databasename))
    return cursor.fetchall()


connection = openconnection('example.db')
conn = connection[0]
cursor = connection[1]
c = cursor
# Statement Create Table
# c.execute("DROP TABLE main")
c.execute("CREATE TABLE IF NOT EXISTS main (link text, text text, doctype text)")
c.execute("CREATE TABLE IF NOT EXISTS keywords (link text, keyword text)")
# Truncate
# truncateDatabase(c, 'main')
# truncateDatabase(c, 'keywords')

# Statement Insert a precise values
# insertData(c,'link',('keyword1', 'keyword2'),'text','kfw_sth')
# insertData(c, '/pathToSomeWhere',('Flo','Badjosh'), 'Hallo Hallo', 'chat')


# Data as array
print(selectAllPreciseByKeyword(cursor, 'keyword1'))
print(selectLinkPreciseByKeyword(cursor, 'keyword1'))
pprint.pprint(selectAllIncludingKeyword(cursor, 'keyword'))
pprint.pprint(selectLinkIncludingKeyword(cursor, 'keyword'))
pprint.pprint(selectLinkIncludingKeyword(cursor, 'JOsh'))
pprint.pprint(selectAll(cursor, 'main'))

# handle end of connection
closeConnection(conn)
