import pandas as pd
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import *
from collections import Counter
import tkinter as tk
from matplotlib.patches import Circle
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from os import path
import mpl_toolkits.mplot3d.art3d as art3d


ObjectList = list()


class Pixel:
    x = int
    y = int
    RGB = (int, int, int)


class Object:
    x = int
    y = int
    z = int
    typeClass = str
    distance = float


def GetDistance(fromTheObject, toTheObject):
    return float(math.sqrt(((toTheObject.x - fromTheObject.x) ** 2) +
                           ((toTheObject.y - fromTheObject.y) ** 2) +
                           ((toTheObject.z - fromTheObject.z) ** 2)))


def GetImagePixelData(imageName):
    im = Image.open(imageName)
    pix = im.load()
    xAxis, yAxis = im.size
    pixelData = list()
    for x in range(xAxis):
        for y in range(yAxis):
            pixel = Pixel()
            if pix[x, y] != (255, 255, 255) and pix[x, y] != (255, 255, 255, 255):
                pixel.x = x
                pixel.y = y
                pixel.RGB = pix[x, y]
                pixelData.append(pixel)
    return pixelData


def GetIntersection(name):
    imageData = GetImagePixelData(f'Images/{name}.png')
    firstProbeData = GetImagePixelData('Probes/FirstProbe.png')
    secondProbeData = GetImagePixelData('Probes/SecondProbe.png')
    thirdProbeData = GetImagePixelData('Probes/ThirdProbe.png')
    intersectionPixel = array([[]])
    probesData = list()
    probesData.append(firstProbeData)
    probesData.append(secondProbeData)
    probesData.append(thirdProbeData)
    for imagePixel in imageData:
        for probes in probesData:
            for probesPixel in probes:
                if (imagePixel.x == probesPixel.x) and (imagePixel.y == probesPixel.y):
                    if probes == firstProbeData:
                        probe = 'First probe'
                    elif probes == secondProbeData:
                        probe = 'Second probe'
                    elif probes == thirdProbeData:
                        probe = 'Third probe'
                    else:
                        probe = None
                    intersectionPixel = append(intersectionPixel, [probe, imagePixel])
    return intersectionPixel


def DataFrames(df):
    if path.isfile('Points.xlsx'):
        dataExcel = pd.read_excel('Points.xlsx')
        df = pd.concat([dataExcel, df])
    with pd.ExcelWriter('Points.xlsx') as writer:
        df.to_excel(writer, index=False)


def GetClassName(firstProbeCount, secondProbeCount, thirdProbeCount, radius):
    GetObjectsFromExcel(firstProbeCount, secondProbeCount, thirdProbeCount)
    radius, includedObjects = SearchIncludedRadiusFeatureSpace(radius)

    obj = GetClass(includedObjects, radius)
    return radius, obj


def GetClass(featureSpaces, radius):
    className = list()
    for featureSpace in featureSpaces:
        className.append(featureSpace.typeClass)
    value = Counter(className).most_common(3)
    print(value)
    if value.__len__() == 1:
        return value[0][0]
    elif value.__len__() > 1:
        counts = list()
        for index in range(value.__len__()):
            counts.append(value[index][1])
        if Counter(counts).__len__() == value.__len__():
            return value[0][0]
        elif counts[0] > Counter(counts).most_common(1)[0][0]:
            return value[0][0]
        else:
            count = Counter(counts).most_common(1)[0][0]
            indexes = list((i for i, e in enumerate(counts) if e == count))
            classNamesIncludedInRadius = list()
            for index in indexes:
                classNamesIncludedInRadius.append(value[index][0])
            nearestPointDistance = radius
            nearestFeatureSpace = Object()
            for featureSpace in featureSpaces:
                if featureSpace.typeClass in classNamesIncludedInRadius and featureSpace.distance < nearestPointDistance:
                    nearestPointDistance = featureSpace.distance
                    nearestFeatureSpace = featureSpace
            return nearestFeatureSpace


def GetProbCounts(inters):
    probesName = list()
    for probeName in inters:
        probesName.append(probeName)
    return probesName.count('First probe'), probesName.count('Second probe'), probesName.count('Third probe')


def GetObjectsFromExcel(x, y, z):
    nullObject = Object()
    nullObject.x = x
    nullObject.y = y
    nullObject.z = z
    if path.isfile('Points.xlsx'):
        dataExcel = pd.read_excel('Points.xlsx').values
        for data in dataExcel:
            obj = Object()
            obj.x = data[1]
            obj.y = data[2]
            obj.z = data[3]
            obj.typeClass = data[4]
            obj.distance = GetDistance(nullObject, obj)
            ObjectList.append(obj)


def SearchIncludedRadiusFeatureSpace(radius):
    includedRadiusFeatureSpace = list()
    while True:
        for obj in ObjectList:
            if float(obj.distance) <= radius:
                includedRadiusFeatureSpace.append(obj)

        if includedRadiusFeatureSpace.__len__() == 0:
            print("Ни одна из точек не входит в заданный радиус!\nРадиус будет увеличен!")
            radius += 1
            print("Радиус поиска: " + str(radius))
        else:
            return radius, includedRadiusFeatureSpace


def GetColorAndSymbolForFeatureSpace(obj):
    if obj == "Г":
        color = 'r'
    elif obj == "Б":
        color = 'g'
    elif obj == "Н":
        color = 'b'
    else:
        color = 'k'
    return color


figure = plt.figure(figsize=(6, 4), dpi=125)
ThreeDimensionalSpacePlot = figure.add_subplot(projection='3d')


def GetWindows():
    dataExcel = None
    if path.isfile('Points.xlsx'):
        dataExcel = pd.read_excel('Points.xlsx').values
    root = tk.Tk()
    root.resizable(False, False)
    for data in dataExcel:
        c = GetColorAndSymbolForFeatureSpace(data[4])
        if c == '':
            continue
        ThreeDimensionalSpacePlot.scatter(data[1], data[2], data[3], color=c)
    scatter = FigureCanvasTkAgg(figure, root)
    scatter.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    root.mainloop(0)
    plt.show()


def DrawingCircle(x, y, z, radius):
    drawObjectZ = Circle((x, y), radius=radius, fill=False, color="black")
    drawObjectX = Circle((y, x), radius=radius, fill=False, color="black")
    ThreeDimensionalSpacePlot.add_patch(drawObjectZ)
    ThreeDimensionalSpacePlot.add_patch(drawObjectX)
    art3d.pathpatch_2d_to_3d(drawObjectX, z=z, zdir='x')
    art3d.pathpatch_2d_to_3d(drawObjectZ, z=z, zdir='z')
    return None


def DrawingLineBetweenFeatureSpace(firstX, firstY, firstZ, second):
    ThreeDimensionalSpacePlot.plot3D([firstX, second.x], [firstY, second.y], [firstZ, second.z], color='k')


def DrawingLineBetweenFeatureSpace1(firstX, firstY, firstZ, secondX, secondY, secondZ):
    ThreeDimensionalSpacePlot.plot3D([firstX, secondX], [firstY, secondY], [firstZ, secondZ], color='k')


if __name__ == '__main__':
    imgName = 'H'
    radius = 2
    intersection = GetIntersection(imgName)
    firstProb, secondProb, thirdProb = GetProbCounts(intersection)
    radius, className = GetClassName(firstProb, secondProb, thirdProb, radius)

    if className is Object:
        data = pd.DataFrame([[imgName, firstProb, secondProb, thirdProb, className.typeClass]],
                            columns=['Name', 'Probe 1', 'Probe 2', 'Probe 3', 'Class'])
        DrawingLineBetweenFeatureSpace(firstProb, secondProb, thirdProb, className)
    else:
        data = pd.DataFrame([[imgName, firstProb, secondProb, thirdProb, className]],
                            columns=['Name', 'Probe 1', 'Probe 2', 'Probe 3', 'Class'])
        DrawingCircle(firstProb, secondProb, thirdProb, radius)

    DataFrames(data)
    GetWindows()
