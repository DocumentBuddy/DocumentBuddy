files = [#"../exampleData/Unternehmensbefragung/Unternehmensbefragung-2017-–-Kreditzugang-bestenfalls-stabil.pdf",
    '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']

from textextraction import extract_frompdf
from text_modeling import *
from api.sqlite import Sqlite
import time

sql = Sqlite()

i = 0
train_model(files)
for file in files:
    i += 1
    #print(extract_frompdf.get_metadata(file))
    pdf = extract_frompdf.extract_text(file)
    text = pdf['content'].strip()
    doctype = file.rsplit(".", 1)[1]
    pages = int(pdf['metadata']['xmpTPg:NPages'])
    keywords = get_topics("test.pickle", "pickck.pkl", doc_id="doc"+str(i))
    entities = get_entities("pickck.pkl", doc_id="doc"+str(i))
    summary = get_summary(text=text, lang="german", count=10)
    date = extract_frompdf.get_creation_date(file)
    sql.insert_data(file[2:], keywords, summary, doctype, toc="", author="",
                    name_entities=entities, pages=pages, date=date)
    #sql.insert_data("a", ["a"], "a", "a", toc="a", author="a",
    #                name_entities=["a"], pages=0, date="a")

sql.close_connection()
    #link, keywords, text, doctype, toc, author, name_entities, pages, date