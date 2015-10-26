from PIL import Image, ImageDraw, ImageChops
import math, operator


def drawPoly(polygonsAndColors, imgHeight, imgWidth):
    base = Image.new('RGB', (imgWidth, imgHeight), "white")
    drw = ImageDraw.Draw(base, 'RGBA')

    for polygonsAndColors in polygonsAndColors:
        drw.polygon(polygonsAndColors[0], tuple(polygonsAndColors[1].astype(int)))
    del drw

    base.show()

def getPolyImage(polygonsAndColors, imgHeight, imgWidth):
    base = Image.new('RGB', (imgWidth, imgHeight), "white")
    drw = ImageDraw.Draw(base, 'RGBA')

    for polygonsAndColors in polygonsAndColors:
        drw.polygon(polygonsAndColors[0], tuple(polygonsAndColors[1].astype(int)))
    del drw

    return base

def rmsdiff(im1, im2):
    "Calculate the root-mean-square difference between two images"
    diff = ImageChops.difference(im1, im2)
    h = diff.histogram()
    sq = (value*((idx%256)**2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    rms = math.sqrt(sum_of_squares/float(im1.size[0] * im1.size[1]))
    return rms

def loadImage(path):
    return Image.open(path)
