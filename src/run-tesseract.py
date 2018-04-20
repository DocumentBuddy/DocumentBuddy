import pytesseract
import pypandoc
from PIL import Image
import os
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

def faster_bradley_threshold(image, threshold=75, window_r=5):
    percentage = threshold / 100.
    window_diam = 2*window_r + 1
    # convert image to numpy array of grayscale values
    img = np.array(image.convert('L')).astype(np.float)  # float for mean precision
    # matrix of local means with scipy
    means = ndimage.uniform_filter(img, window_diam)
    # result: 0 for entry less than percentage*mean, 255 otherwise
    height, width = img.shape[:2]
    result = np.zeros((height,width), np.uint8)   # initially all 0
    result[img >= percentage * means] = 255       # numpy magic :)
    # convert back to PIL image
    return Image.fromarray(result)


# Load Image
img = Image.open('datakibots.png')

# Image binarization
# Bradley, Gatos, Otsu,
# http://gamera.informatik.hsnr.de/docs/gamera-docs/binarization.html
# https://pdfs.semanticscholar.org/372a/3ae802610e1a1564f7836f078e976a3db16c.pdf
# http://www.ijecs.in/issue/v3-i3/9%20ijecs.pdf
th_img = faster_bradley_threshold(img)
th2_img = faster_bradley_threshold(img, threshold=85)
filename = "{}.png".format(os.getpid())
th2_img.save(filename, "png")




# OCR
text = pytesseract.image_to_string(Image.open(filename))
text_alt = pytesseract.image_to_string(img) # Image.open('test.jpg')
os.remove(filename)


# Post Processing
text = text.replace(" ", "").replace("|", "I").replace("]","J").replace("1","I")
print(text)

