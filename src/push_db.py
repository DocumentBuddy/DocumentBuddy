files = [#"../exampleData/Unternehmensbefragung/Unternehmensbefragung-2017-–-Kreditzugang-bestenfalls-stabil.pdf",
    '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']

from textextraction import extract_frompdf
from api.sqlite import Sqlite

sql = Sqlite()

for file in files:
    print(extract_frompdf.get_metadata(file))
    text = extract_frompdf.extract_text(file)
    sql.insert_data_in_main(file, "", "pdf", text, "", "", 23, "")