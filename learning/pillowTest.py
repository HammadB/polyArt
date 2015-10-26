from PIL import Image, ImageDraw
import numpy as np
from draw import drawPoly

polygons = []

numpoly, numverts, maxCenterDis = 10000, 4, 250
centers = 400 * (np.random.random((numpoly,2)))
for center in centers:
    shifts = maxCenterDis * np.random.random(numverts*2)
    poly = []
    i = 0
    while i < len(shifts):
        point = (center[0] + shifts[i], center[1] + shifts[i+1])
        poly.append(point)
        i += 2
    polygons.append(poly)

colors = 255 * np.random.random((numpoly, 4))

drawPoly(polygons, colors, 400, 400)
