"""

import fitz

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
#extract_images('../exampleData/Unternehmensbefragung/Unternehmensbefragung-2001-kurz.pdf')
import pandas as pd
df = pd.read_table("textextraction/city_list.txt")
cities_global = df["nm"].str.lower().tolist()
zip_csv = pd.read_csv("textextraction/German-Zip-Codes.csv", sep=";", header=0)
cities_germany = zip_csv["Ort"].drop_duplicates() #?
print(cities_germany) #?
german_states = zip_csv["Bundesland"].drop_duplicates().str.lower().tolist()
with open('textextraction/regions-german') as f:
    german_reg = f.readlines()

places = cities_global + german_states + german_reg