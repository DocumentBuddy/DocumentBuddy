from extract_frompdf import extract_text

files = ['../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
         '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']

ini = 0
corpus = {}
for file in files:
    ini += 1
    corpus['doc' + str(ini)] = extract_text(file)