# -*- coding: utf-8 -*-
#import fitz
import re
import platform
import os
from tika import parser
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import PyPDF2


def extract_text(path):
    try:
        return parser.from_file(path, headers={'charset': 'utf8'})
    except UnicodeEncodeError:
        return ""
        pass
        #with open(path, "rb") as pdf_file:
        #    read_pdf = PyPDF2.PdfFileReader(pdf_file)
        #    page_content = ""
        #    for i in range(read_pdf.getNumPages()):
        #        page = read_pdf.getPage(i)
        #        page_content += page.extractText()
    #udata = text.decode("utf-8")
    #data=udata.encode("latin-1","ignore")

def get_metadata(path):
    fp = open(path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    return doc.info[0] if not len(doc.info) == 0 else {}

"""
def extract_images(path):
    checkXO = r"/Type(?= */XObject)"       # finds "/Type/XObject"
    checkIM = r"/Subtype(?= */Image)"      # finds "/Subtype/Image"

    doc = fitz.open(path)
    imgcount = 0
    lenXREF = doc._getXrefLength()         # number of objects - do not use entry 0!

    # display some file info
    print("file: %s, pages: %s, objects: %s" % (path, len(doc), lenXREF-1))

    for i in range(1, lenXREF):            # scan through all objects
        text = doc._getObjectString(i)     # string defining the object
        isXObject = re.search(checkXO, text)    # tests for XObject
        isImage   = re.search(checkIM, text)    # tests for Image
        if not isXObject or not isImage:   # not an image object if not both True
            continue
        imgcount += 1
        pix = fitz.Pixmap(doc, i)          # make pixmap from image
        if pix.n < 5:                      # can be saved as PNG
            pix.writePNG("img-%s.png" % (i,))
        else:                              # must convert the CMYK first
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.writePNG("img-%s.png" % (i,))
            pix0 = None                    # free Pixmap resources
        pix = None                         # free Pixmap resources

"""
def get_creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime
if __name__ == "__main__":
    # for sentence in get_summary(text):
    #    print(sentence)
    filepath = "../exampleData/Unternehmensbefragung/Unternehmensbefragung-2017-–-Kreditzugang-bestenfalls-stabil.pdf"
    print(get_metadata(filepath))