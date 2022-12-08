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


class Pixel:
    x = int
    y = int
    RGB = (int, int, int)


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


def GetA(name):
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


def GetProbCounts(inters):
    probesName = list()
    for probeName in inters:
        probesName.append(probeName)
    return probesName.count('First probe'), probesName.count('Second probe'), probesName.count('Third probe')


if __name__ == '__main__':
    imagesName = ['Б1', 'Б2', 'Б3', 'Б4', 'Б5', 'Г1', 'Г2', 'Г3', 'Г4', 'Г5', 'Н1', 'Н2', 'Н3', 'Н4', 'Н5']
    data = pd.DataFrame(columns=['Name', 'Probe 1', 'Probe 2', 'Probe 3', 'Class'])
    for name in imagesName:
        intersection = GetA(name)
        probe1, probe2, probe3 = GetProbCounts(intersection)
        ndata = pd.DataFrame([[name, probe1, probe2, probe3, name[0]]],
                            columns=['Name', 'Probe 1', 'Probe 2', 'Probe 3', 'Class'])
        data = pd.concat([data, ndata])

    with pd.ExcelWriter('Points.xlsx') as writer:
        data.to_excel(writer, index=False)