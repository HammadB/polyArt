import numpy as np
from draw import *
from random import randint
import random
from copy import deepcopy


def seed(numpoly, numverts, maxCenterDis, imageSize):
    polygons = []
    centers = imageSize * (np.random.random((numpoly,2)))
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

    return zip(polygons, colors)

#Generates popSize seeds using seed - unused atm
def seedPopulation(popSize, maxNumPoly, maxNumVerts, centerDis, imageSize):
    population = []
    for i in range(popSize):
        numPoly = randint(50, maxNumPoly)
        numVerts = randint(3, maxNumVerts)
        currSeed = seed(numPoly, numVerts, centerDis, imageSize)
        population.append(currSeed)
    return population

def translatePolygon(polygon, maxX, maxY):
    x_shift = randint(0, maxX) * random.choice([-1, 1])
    y_shift = randint(0, maxY) * random.choice([-1, 1])
    for i in range(len(polygon)):
        polygon[i] = (polygon[i][0] + x_shift, polygon[i][1] + y_shift)

def shiftColor(rgba, maxShift):
    numChannels = random.choice([1,2,3,4]) 
    whichChannels = random.sample([0,1,2,3], numChannels) #R?G?B?A?
    for i in range(numChannels):
        rgba[whichChannels[i]] += randint(-maxShift, maxShift)
        #wrap values around..try?
        if rgba[whichChannels[i]] > 255:
            rgba[whichChannels[i]] -= 255
        if rgba[whichChannels[i]] < 0:
            rgba[whichChannels[i]] = 255 - (-1)*rgba[whichChannels[i]]

def scalePolygon(polygon, maxX, maxY):
    numVerts = len(polygon)
    numVertsToModify = random.choice(range(1, numVerts)) #choose to modify 1 to N vertices
    whichVertsToModify = random.sample(range(numVerts), numVertsToModify)
    x_shift = randint(0, maxX) * random.choice([-1, 1])
    y_shift = randint(0, maxX) * random.choice([-1, 1])
    for i in range(numVertsToModify):
        vertIndex = whichVertsToModify[i]
        polygon[vertIndex] = (polygon[vertIndex][0] + x_shift, polygon[vertIndex][1] + y_shift) 

def addPolygon(polygonsAndColors, numverts, maxCenterDis, imageWidth, imageHeight):
    imageSize = max(imageWidth, imageHeight)
    center = imageSize * (np.random.random((1,2)))[0]
    shifts = maxCenterDis * np.random.random(numverts*2)
    poly = []
    i = 0
    while i < len(shifts):
        point = (center[0] + shifts[i], center[1] + shifts[i+1])
        poly.append(point)
        i += 2
    color = 255 * np.random.random((1, 4))[0]

    polygonsAndColors.append([poly, color])

def removePolygon(polygonsAndColors):
    polygonsAndColors.pop(randint(0, len(polygonsAndColors) - 1))


def mutateCitizen(polygonsAndColors, numverts, maxCenterDis, imageWidth, imageHeight, currMinRms=0):
    translateThreshold = 10
    shiftColorThreshold = 10
    scaleThreshold = 10
    addThreshold = 10

    # if currMinRms < 35:
    #     addThreshold = 40
    removeThreshold = 10

    removeProb = randint(0, 100)
    if removeProb < removeThreshold and len(polygonsAndColors) > 5:
        removePolygon(polygonsAndColors)

    polygonsAndColorsToModify = random.sample(polygonsAndColors, randint(1, 5))
    for polygonsAndColor in polygonsAndColorsToModify:

        translateProb = randint(0, 100)
        if translateProb < translateThreshold:
            translatePolygon(polygonsAndColor[0], imageWidth, imageHeight)

        shiftColorProb = randint(0, 100)
        if shiftColorProb < shiftColorThreshold:
            shiftColor(polygonsAndColor[1], 255)

        scaleProb = randint(0, 100)
        if scaleProb < scaleThreshold:
            scalePolygon(polygonsAndColor[0], imageWidth, imageHeight)


    addProb = randint(0, 100)
    if addProb < addThreshold:
        addPolygon(polygonsAndColors, numverts, maxCenterDis, imageWidth, imageHeight)

    return polygonsAndColors

def go(path):
    target = loadImage(path)
    target.show()
    width, height = target.size
    minDim = min(width, height)/16
    numverts = 5

    minCitizen = seed(10, numverts, minDim/8, height)
    minImage = getPolyImage(minCitizen, height, width)
    minRms = rmsdiff(minImage, target)

    try:
        for i in range(904000):
            currCitizen = mutateCitizen(deepcopy(minCitizen), numverts, minDim/8, width, height, minRms)
            currImage = getPolyImage(currCitizen, height, width)
            rms = rmsdiff(currImage, target)
            if rms < minRms:
                minRms = rms
                minImage = currImage
                minCitizen = currCitizen
                print("MIN RMS:" + str(minRms) + " Iter: " + str(i) + "Num Poly: " + str(len(minCitizen)))
    except:
        minImage.show()
        exit()
    minImage.show()
