# Workflow for the DocumentBuddy
#from extract_frompdf import extract_text, extract_images
from textextraction import extract_frompdf

if __name__ == '__main__':
    files = ['../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2002-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2003-2004-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2005-kurz.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2006-kurz-D.pdf',
             '../exampleData/Unternehmensbefragung/Unternehmensbefragung-2008-Kurz-Deutsch.pdf']
    text = extract_frompdf.extract_text(files[0])
    if not text:
        extract_frompdf.extract_images(files[0])
    print(text.strip())
